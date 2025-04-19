# resource_fetcher.py

import boto3
from botocore.exceptions import ClientError
import logging

from aws_unused_tracker.config import ENABLE_LOGGING

if ENABLE_LOGGING:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_all_regions():
    """
    Returns a list of all active AWS regions.
    """
    try:
        ec2 = boto3.client('ec2')
        regions_response = ec2.describe_regions(AllRegions=False)
        return [region['RegionName'] for region in regions_response['Regions']]
    except ClientError as e:
        logging.error(f"Error fetching regions: {e}")
        return []


def fetch_ec2_instances(region):
    """
    Returns a list of running EC2 instances in the given region.
    Each instance contains: InstanceId, Region, State, Name
    """
    instances = []
    try:
        ec2 = boto3.client('ec2', region_name=region)
        paginator = ec2.get_paginator('describe_instances')
        for page in paginator.paginate():
            for reservation in page['Reservations']:
                for instance in reservation['Instances']:
                    if instance['State']['Name'] == 'running':
                        name_tag = next(
                            (tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name'),
                            'N/A'
                        )
                        instances.append({
                            'InstanceId': instance['InstanceId'],
                            'Region': region,
                            'State': 'running',
                            'Name': name_tag
                        })
        return instances
    except ClientError as e:
        logging.warning(f"Failed to fetch EC2 in {region}: {e}")
        return []

