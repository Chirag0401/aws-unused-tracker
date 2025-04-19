# ebs_analyzer.py

import boto3
from datetime import datetime, timezone, timedelta
import logging

from aws_unused_tracker.config import EBS_READ_THRESHOLD, EBS_WRITE_THRESHOLD, METRIC_LOOKBACK_DAYS, METRIC_PERIOD, ENABLE_LOGGING

if ENABLE_LOGGING:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_all_ebs_volumes(region):
    """
    Fetches all EBS volumes in the given region.
    Returns a list with volume metadata.
    """
    volumes_data = []
    ec2 = boto3.client('ec2', region_name=region)
    cloudwatch = boto3.client('cloudwatch', region_name=region)

    paginator = ec2.get_paginator('describe_volumes')
    for page in paginator.paginate():
        for volume in page['Volumes']:
            volume_id = volume['VolumeId']
            state = volume['State']
            size = volume['Size']
            create_time = volume['CreateTime']
            attachments = volume.get('Attachments', [])
            attached = bool(attachments)

            age_days = (datetime.now(timezone.utc) - create_time).days

            read_ops = get_average_metric(cloudwatch, volume_id, 'VolumeReadOps')
            write_ops = get_average_metric(cloudwatch, volume_id, 'VolumeWriteOps')

            is_idle = (not attached) or (read_ops < EBS_READ_THRESHOLD and write_ops < EBS_WRITE_THRESHOLD)

            volumes_data.append({
                'VolumeId': volume_id,
                'Region': region,
                'SizeGB': size,
                'Attached': attached,
                'ReadOps': int(read_ops),
                'WriteOps': int(write_ops),
                'AgeDays': age_days,
                'Status': 'Idle' if is_idle else 'Active'
            })

    return volumes_data


def get_average_metric(cloudwatch, volume_id, metric_name):
    """
    Get average read/write ops over the last N days.
    """
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=METRIC_LOOKBACK_DAYS)

    try:
        result = cloudwatch.get_metric_statistics(
            Namespace='AWS/EBS',
            MetricName=metric_name,
            Dimensions=[{'Name': 'VolumeId', 'Value': volume_id}],
            StartTime=start_time,
            EndTime=end_time,
            Period=METRIC_PERIOD,
            Statistics=['Sum'],
            Unit='Count'
        )
        datapoints = result.get('Datapoints', [])
        if not datapoints:
            return 0
        return sum(dp['Sum'] for dp in datapoints) / len(datapoints)
    except Exception as e:
        logging.warning(f"Error fetching {metric_name} for volume {volume_id}: {e}")
        return 0

