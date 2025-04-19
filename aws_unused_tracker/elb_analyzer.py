# elb_analyzer.py

import boto3
from datetime import datetime, timedelta
import logging
from aws_unused_tracker.config import ELB_REQUEST_THRESHOLD, METRIC_LOOKBACK_DAYS, METRIC_PERIOD, ENABLE_LOGGING

if ENABLE_LOGGING:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def analyze_elbs(region):
    elbv2 = boto3.client('elbv2', region_name=region)
    cloudwatch = boto3.client('cloudwatch', region_name=region)

    idle_elbs = []

    try:
        paginator = elbv2.get_paginator('describe_load_balancers')
        for page in paginator.paginate():
            for lb in page['LoadBalancers']:
                lb_name = lb['LoadBalancerName']
                lb_arn = lb['LoadBalancerArn']
                lb_type = lb['Type']
                created_time = lb['CreatedTime']
                age_days = (datetime.utcnow() - created_time.replace(tzinfo=None)).days

                request_count = get_average_request_count(cloudwatch, lb_name, lb_type)

                is_idle = request_count < ELB_REQUEST_THRESHOLD

                idle_elbs.append({
                    'LoadBalancerName': lb_name,
                    'Region': region,
                    'Type': lb_type,
                    'RequestCount': int(request_count),
                    'AgeDays': age_days,
                    'Status': 'Idle' if is_idle else 'Active'
                })

    except Exception as e:
        logging.warning(f"Error analyzing ELBs in {region}: {e}")

    return idle_elbs


def get_average_request_count(cloudwatch, lb_name, lb_type):
    """
    Fetch average RequestCount over the past 7 days for ALB/NLB
    """
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=METRIC_LOOKBACK_DAYS)

    metric_name = "RequestCount"
    namespace = "AWS/ApplicationELB" if lb_type == "application" else "AWS/NetworkELB"

    try:
        response = cloudwatch.get_metric_statistics(
            Namespace=namespace,
            MetricName=metric_name,
            Dimensions=[{'Name': 'LoadBalancer', 'Value': lb_name}],
            StartTime=start_time,
            EndTime=end_time,
            Period=METRIC_PERIOD,
            Statistics=['Sum'],
            Unit='Count'
        )
        datapoints = response.get('Datapoints', [])
        if not datapoints:
            return 0
        return sum(dp['Sum'] for dp in datapoints) / len(datapoints)

    except Exception as e:
        logging.warning(f"Error fetching RequestCount for {lb_name}: {e}")
        return 0

