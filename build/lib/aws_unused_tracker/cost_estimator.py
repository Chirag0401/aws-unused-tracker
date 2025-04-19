from botocore.exceptions import ClientError
import boto3
import datetime
import logging
from collections import defaultdict
from aws_unused_tracker.config import ENABLE_LOGGING

if ENABLE_LOGGING:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_monthly_service_cost():
    """
    Fetches total cost for the current month by AWS Service.
    Cost Explorer must be enabled and permissions granted.
    """
    ce = boto3.client('ce', region_name='us-east-1')  # Cost Explorer only works in us-east-1

    end = datetime.date.today()
    start = end.replace(day=1)

    try:
        response = ce.get_cost_and_usage(
            TimePeriod={
                'Start': start.strftime('%Y-%m-%d'),
                'End': end.strftime('%Y-%m-%d')
            },
            Granularity='MONTHLY',
            Metrics=['UnblendedCost'],
            GroupBy=[{
                'Type': 'DIMENSION',
                'Key': 'SERVICE'
            }]
        )

        service_costs = {}
        results = response.get('ResultsByTime', [])
        if results:
            for group in results[0]['Groups']:
                service = group['Keys'][0]
                cost = float(group['Metrics']['UnblendedCost']['Amount'])
                service_costs[service] = round(cost, 2)

        return service_costs

    except ClientError as e:
        if e.response['Error']['Code'] == "AccessDeniedException":
            print("\n⚠️  Cost Explorer access denied.")
            print("👉 To enable cost reporting, make sure:")
            print("   - Cost Explorer is enabled in the AWS Console")
            print("   - Your IAM role has the permission: ce:GetCostAndUsage\n")
        else:
            print(f"\n⚠️  Unexpected AWS error: {e}")
        return {}

    except Exception as e:
        print(f"\n⚠️  Unexpected error while fetching cost data: {e}\n")
        return {}

