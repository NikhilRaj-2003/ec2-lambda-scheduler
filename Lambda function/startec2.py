import boto3
from datetime import datetime

# Configuration
region = 'ap-south-1'
instances = ['i-036bb14d2a7a28941']
sns_topic_arn = 'arn:aws:sns:ap-south-1:530424100396:startec2'  # replace with your actual SNS topic ARN

# Clients
ec2 = boto3.client('ec2', region_name=region)
sns = boto3.client('sns', region_name=region)

def lambda_handler(event, context):
    ec2.start_instances(InstanceIds=instances)
    print('Started your instance: ' + str(instances))
    
    # Compose notification
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = f"✅ EC2 instance {instances[0]} started at {timestamp}."
    
    # Send notification via SNS
    sns.publish(
        TopicArn=sns_topic_arn,
        Subject='EC2 Instance Started',
        Message=message
    )

    return {
        'statusCode': 200,
        'body': message
    }
