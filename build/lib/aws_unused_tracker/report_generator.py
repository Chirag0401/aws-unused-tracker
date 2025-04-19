# report_generator.py

import os
import json
import csv
from tabulate import tabulate
from aws_unused_tracker.config import EXPORT_JSON, EXPORT_CSV, EXPORT_DIR

def print_report_table(data, headers, title):
    """
    Prints a formatted table in the terminal with a custom title and headers.
    """
    if not data:
        print(f"\n⚠️  No data found for {title}.")
        return
    print(f"\n📊 {title}:\n")
    print(tabulate(data, headers=headers, tablefmt="grid"))


def export_to_json(data, filename, headers):
    """
    Exports data to a JSON file.
    """
    os.makedirs(EXPORT_DIR, exist_ok=True)
    filepath = os.path.join(EXPORT_DIR, filename)
    json_data = [dict(zip(headers, row)) for row in data]
    with open(filepath, 'w') as f:
        json.dump(json_data, f, indent=4)
    print(f"[✓] Exported JSON: {filepath}")


def export_to_csv(data, filename, headers):
    """
    Exports data to a CSV file.
    """
    os.makedirs(EXPORT_DIR, exist_ok=True)
    filepath = os.path.join(EXPORT_DIR, filename)
    with open(filepath, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in data:
            writer.writerow(row)
    print(f"[✓] Exported CSV: {filepath}")


def generate_report(data, resource_type, output_format="all", dry_run=False):
    """
    Generates the report for a specific resource type.
    """
    resource_map = {
        "ec2": {
            "title": "EC2 Idle Instance Report",
            "headers": ["Instance ID", "Instance Name", "Region", "Avg CPU (%)", "Network I/O (MB)", "Status", "Reason"],
            "filename_json": "ec2_idle_report.json",
            "filename_csv": "ec2_idle_report.csv"
        },
        "ebs": {
            "title": "EBS Idle Volume Report",
            "headers": ["Volume ID", "Region", "Size (GB)", "Attached", "Read Ops", "Write Ops", "Age (Days)", "Status"],
            "filename_json": "ebs_idle_report.json",
            "filename_csv": "ebs_idle_report.csv"
        },
        "elb": {
            "title": "ELB Idle Report",
            "headers": ["Load Balancer", "Region", "Type", "Request Count", "Age (Days)", "Status"],
            "filename_json": "elb_idle_report.json",
            "filename_csv": "elb_idle_report.csv"
        }
    }

    if resource_type not in resource_map:
        print(f"[!] Unknown resource type: {resource_type}")
        return

    config = resource_map[resource_type]
    if output_format in ["all", "table"]:
        print_report_table(data, config["headers"], config["title"])

    if not dry_run:
        if output_format in ["all", "json"] and EXPORT_JSON:
            export_to_json(data, config["filename_json"], config["headers"])
        if output_format in ["all", "csv"] and EXPORT_CSV:
            export_to_csv(data, config["filename_csv"], config["headers"])

