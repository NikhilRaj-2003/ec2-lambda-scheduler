import boto3
from datetime import datetime

# Configuration
region = 'ap-south-1'
instances = ['i-036bb14d2a7a28941']
sns_topic_arn = 'arn:aws:sns:ap-south-1:530424100396:stopec2'  # Replace with your actual SNS topic ARN

# Create clients
ec2 = boto3.client('ec2', region_name=region)
sns = boto3.client('sns', region_name=region)

def lambda_handler(event, context):
    # Stop the instance
    ec2.stop_instances(InstanceIds=instances)
    print('Stopped your instance: ' + str(instances))

    # Prepare and send SNS notification
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = f"EC2 instance {instances[0]} was stopped at {timestamp}."
    sns.publish(
        TopicArn=sns_topic_arn,
        Subject="EC2 Instance Stopped",
        Message=message
    )

    return {
        'statusCode': 200,
        'body': message
    }

