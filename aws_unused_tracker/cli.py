import argparse
from aws_unused_tracker.cost_estimator import get_monthly_service_cost
from aws_unused_tracker.resource_fetcher import get_all_regions, fetch_ec2_instances
from aws_unused_tracker.metric_analyzer import get_ec2_usage_summary
from aws_unused_tracker.idle_detector import classify_instance
from aws_unused_tracker.report_generator import generate_report
from aws_unused_tracker.ebs_analyzer import get_all_ebs_volumes
from aws_unused_tracker.elb_analyzer import analyze_elbs
import logging

from aws_unused_tracker.config import ENABLE_LOGGING

if ENABLE_LOGGING:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_args():
    parser = argparse.ArgumentParser(description="🔎 AWS Unused Resource Tracker")
    parser.add_argument(
        "--region",
        nargs="+",
        help="Specify one or more AWS regions to scan (default: all regions)"
    )
    parser.add_argument(
        "--idle-only",
        action="store_true",
        help="Show only idle resources"
    )
    parser.add_argument(
        "--format",
        choices=["table", "csv", "json", "all"],
        default="all",
        help="Output format: table, csv, json, or all (default)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview report without exporting or calculating cost"
    )

    return parser.parse_args()

def cli():
    args = parse_args()
    ec2_data = []
    ebs_data = []
    elb_data = []

    print("🔍 Starting Unused Resource Tracker...\n")

    regions = args.region if args.region else get_all_regions()
    for region in regions:
        # EC2
        instances = fetch_ec2_instances(region)
        for instance in instances:
            instance_id = instance["InstanceId"]
            instance_name = instance.get("Name", "N/A")
            usage = get_ec2_usage_summary(region, instance_id)
            status, reason = classify_instance(usage["cpu_avg"], usage["network_mb"])
            ec2_data.append([
                instance_id,
                instance_name,
                region,
                usage["cpu_avg"],
                usage["network_mb"],
                status,
                reason
            ])

        # EBS
        ebs_volumes = get_all_ebs_volumes(region)
        for vol in ebs_volumes:
            ebs_data.append([
                vol['VolumeId'],
                vol['Region'],
                vol['SizeGB'],
                vol['Attached'],
                vol['ReadOps'],
                vol['WriteOps'],
                vol['AgeDays'],
                vol['Status']
            ])

        # ELB
        elbs = analyze_elbs(region)
        for lb in elbs:
            elb_data.append([
                lb['LoadBalancerName'],
                lb['Region'],
                lb['Type'],
                lb['RequestCount'],
                lb['AgeDays'],
                lb['Status']
            ])

    # --- Generate Reports ---
    ec2_final = [r for r in ec2_data if (not args.idle_only or r[5] == "Idle")]
    ebs_final = [r for r in ebs_data if (not args.idle_only or r[7] == "Idle")]
    elb_final = [r for r in elb_data if (not args.idle_only or r[5] == "Idle")]
    generate_report(ec2_final, resource_type="ec2", output_format=args.format, dry_run=args.dry_run)
    generate_report(ebs_final, resource_type="ebs", output_format=args.format, dry_run=args.dry_run)
    generate_report(elb_final, resource_type="elb", output_format=args.format, dry_run=args.dry_run)

    # --- Cost Explorer Savings Estimate ---
    print("\n💸 Estimating potential monthly savings...\n")
    cost_data = get_monthly_service_cost()

    ec2_cost = cost_data.get("AmazonEC2", 0.0)
    ebs_cost = cost_data.get("AmazonEBS", 0.0)
    elb_cost = cost_data.get("AmazonElasticLoadBalancing", 0.0)

    idle_ec2_count = sum(1 for row in ec2_data if row[5] == "Idle")
    idle_ebs_count = sum(1 for row in ebs_data if row[7] == "Idle")
    idle_elb_count = sum(1 for row in elb_data if row[5] == "Idle")

    est_savings = 0.0
    summary_lines = []

    def estimate_savings(service_name, total_cost, idle_count, total_count):
        if idle_count == 0 or total_cost == 0 or total_count == 0:
            return 0.0
        avg_cost = total_cost / total_count
        savings = round(avg_cost * idle_count, 2)
        summary_lines.append(f"{service_name:20}: {idle_count} idle → ~${savings}")
        return savings

    est_savings += estimate_savings("EC2 Instances", ec2_cost, idle_ec2_count, len(ec2_data))
    est_savings += estimate_savings("EBS Volumes", ebs_cost, idle_ebs_count, len(ebs_data))
    est_savings += estimate_savings("ELBs", elb_cost, idle_elb_count, len(elb_data))

    print("💡 Potential Monthly Savings Summary")
    print("--------------------------------------")
    for line in summary_lines:
        print(line)
    print(f"{'Total Estimated Savings':20}: ~${round(est_savings, 2)}")
    print("--------------------------------------")


if __name__ == "__main__":
    cli()

