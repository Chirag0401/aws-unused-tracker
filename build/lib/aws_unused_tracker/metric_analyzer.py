# metric_analyzer.py

import boto3
import datetime
import logging
from aws_unused_tracker.config import METRIC_LOOKBACK_DAYS, METRIC_PERIOD, ENABLE_LOGGING

if ENABLE_LOGGING:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_average_metric(region, instance_id, metric_name, stat='Average', unit='Percent'):
    """
    Fetches the average value of a given CloudWatch metric for an EC2 instance.
    """
    cloudwatch = boto3.client('cloudwatch', region_name=region)
    end_time = datetime.datetime.utcnow()
    start_time = end_time - datetime.timedelta(days=METRIC_LOOKBACK_DAYS)

    try:
        response = cloudwatch.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName=metric_name,
            Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
            StartTime=start_time,
            EndTime=end_time,
            Period=METRIC_PERIOD,
            Statistics=[stat],
            Unit=unit
        )

        datapoints = response.get('Datapoints', [])
        if not datapoints:
            return 0.0

        avg_value = sum(dp[stat] for dp in datapoints) / len(datapoints)
        return round(avg_value, 2)

    except Exception as e:
        logging.warning(f"Error fetching {metric_name} for {instance_id} in {region}: {e}")
        return 0.0


def get_ec2_usage_summary(region, instance_id):
    """
    Returns average CPU and total network usage in MB for an EC2 instance.
    """
    cpu_avg = get_average_metric(region, instance_id, 'CPUUtilization', 'Average', 'Percent')
    net_in = get_average_metric(region, instance_id, 'NetworkIn', 'Average', 'Bytes')
    net_out = get_average_metric(region, instance_id, 'NetworkOut', 'Average', 'Bytes')

    network_total_mb = round((net_in + net_out) / (1024 * 1024), 2)  # Convert to MB
    return {
        'cpu_avg': cpu_avg,
        'network_mb': network_total_mb
    }

