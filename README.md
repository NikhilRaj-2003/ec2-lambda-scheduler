“Smart Cloud Management: Auto-Start/Stop EC2 Instances and Receive Notifications”
=================================================================================

![Auto — Shutdown EC2](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*ZAJ9BhaCiWJ2gyzkku5SNQ.png)

[Reference](https://medium.com/@nikhilsiri2003/smart-cloud-management-auto-start-stop-ec2-instances-and-receive-notifications-3b96514f5116)

by [Nikhil Raj A](https://medium.com/@nikhilsiri2003?source=post_page---byline--3b96514f5116---------------------------------------)


**Introduction**
----------------

In AWS (Amazon Web Services), **Elastic Compute Cloud (EC2)** instances are widely used for running applications, websites, and services. However, one common issue many users face is forgetting to shut down unused instances — leading to unnecessary billing.

This project solves that problem by **automatically shutting down idle EC2 instances** if they remain **inactive for more than 5 minutes** and **notifying the user instantly** via email or SMS.
By integrating AWS **CloudWatch**, **Lambda**, and **SNS**, we can build an intelligent, self-managing solution that minimizes costs and ensures no resource goes wasted.

Whether you’re a solo developer, startup, or enterprise team, this mini project is a **simple but powerful way to automate your cloud operations** and improve cost efficiency.

![Simple Architecture of the procedure](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*12WqpH6k7jGMnzGbSqXleA.png)

**What is Lambda ??**
---------------------

**AWS Lambda** is a serverless compute service that allows you to run code without provisioning or managing servers. You simply upload your code, set up a trigger (like an alarm or event), and AWS automatically runs the code for you when needed.

**What is EC2 in AWS ?**
------------------------

**Amazon EC2 (Elastic Compute Cloud)** is a web service that provides resizable computing capacity in the cloud. Think of EC2 as a virtual computer where you can run applications, host websites, or perform any tasks you would normally do on a physical server.

**What is SNS in AWS ?**
------------------------

**Amazon SNS (Simple Notification Service)** is a fully managed messaging service that enables you to send notifications to users or other systems. It can send messages via email, SMS, or push notifications.

**Prerequisites**
-----------------

*   AWS Account
*   Gmail Account

**Step — 1 : Create a IAM Role and Policy**
-------------------------------------------

1.  Go to AWS Management console .
2.  Create a IAM policy and provide EC2 , SNS and also Logs Permissions . Then click on “**create policy”**

```
{
 "Version": "2012-10-17",
 "Statement": [  {
   "Effect": "Allow",
   "Action": [    "logs:CreateLogGroup",
    "logs:CreateLogStream",
    "logs:PutLogEvents"
   ],
   "Resource": "arn:aws:logs:*:*:*"
  },
  {
   "Effect": "Allow",
   "Action": [    "ec2:Start*",
    "ec2:Stop*"
   ],
   "Resource": "*"
  }
 ]
}
```

3. Create a IAM Role by clicking on the “**create role”** and attach that policy to that newly created role. Select Trusted entity type as **“AWS Service”** and also Select use case as “**Lambda”**

![captionless image](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*W2ZcT1KeYd7N5hGAqhzjYg.png)

4. Select and attach the policy that you have created, then click on “**create role” .** A role would be created with the desired permissions required .

![Role created and policy attached](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*rPQYskwmL_1r0CN8C9LITQ.png)

**Step — 2 : Create 2 Lambda Functions for starting and stopping instance**

Stopec2 Function
----------------

1.  Go to AWS Services → **Lambda** and click on ‘**Create function**’.
2.  Choose an **Author from scratch**
3.  Under **Basic information**, enter the following information:
    For **Function name**, enter a name that identifies it as the function that’s used to stop your EC2 instances. For example, “**stopec2**”.
4.  For **Runtime,** choose **Python 3.9**
5.  **Under Permissions,** expand Change default execution role
6.  **Under the Execution role**, choose to **Use an existing role**
7.  **Under Existing role**, choose the **IAM role** that you created
8.  Choose **Create function**
9.  After creating the Lambda Function, go to → Under Code, Code source, copy and paste the below Python code.

```
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
```

> Replace instance — id with your instance id and provide the region which your instance is been running .

10. Aftering altering the code , then click on **“Deploy”** for deploying the code .

Startec2 Function
-----------------

1.  Repeat the steps from 1–9 , but in this function you need to change the code . Because this code used for starting the EC2 instance .

```
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
```

2. Click on “**Deploy”** for deploying the code . And you may also click on “test” for testing the code manually for checking the code performance .

**Step — 3 : Create 2 SNS Topics for start and stop instance notifications**

![Creating SNS topic](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*Wtuwsshb1bgYKR6vsOCGxg.png)

1.  Click on **“Next Step”** and provide the details like **name** and **type** of the SNS . Then click on “**create topic”**

![captionless image](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*kv4szMJIIupyxTN7ZWHL1Q.png)

2. Create another topic with **“standard”** as its type and also Provide the name as “**stopec2rule” .** Click on “**create topic”**

![captionless image](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*A4epTYII9JqwWWXltJ4jHA.png)

3. After creation of the topics , create subscription for both the topics . Where you need to provide the type of the notifications to be received like “Email , SMS or Email Json” etc . Provide your mail — id if you wanna be notified via mail .

4. Later a Mail will be sent to your EMail for **confirming the subscription,** so that the notifications will be forwarded to the email which you have confirmed .

**Step — 4 : Create 2 Rules for Start and stop of EC2 instance under EventBridge Scheduler**
--------------------------------------------------------------------------------------------

startec2Rule
------------

1.  Go to the Lambda Function(startec2) and click on “**add Trigger” .**
2.  Select “**EventBridge(cloudwatch Events)”** as the trigger and provide the details .
3.  create a new rule and provide a name(**startec2rule**) for the rule .
4.  Select “**schedule expression”** as rule type.
5.  Provide the schedule expression in the “**cron” format .** I have given a cron expression where the EC2 instance must start running at **8:25pm** of **23 may 2025 .** You can also the cron expression based on your comfort.
6.  click on “**Add”** for adding a trigger .

![eventbridge as lambda Trigger](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*GLNGv3-aFWLT81Sh-h5Slg.png)

stopec2Rule
-----------

1.  Repeat the steps from 1–4 , in the 5th step you need to add a different cron expression for stopping the ec2 instance .
2.  Provide the schedule expression in the “**cron” format .** I have given a cron expression where the EC2 instance must start running at **8:40 pm** of **23 may 2025 .** You can also the cron expression based on your comfort.

![eventbridge as lambda Trigger](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*3LH5Xm80jGbndl_Wr-85Ig.png)

**Results**
-----------

> _Starting of the EC2 instance and getting notified about the starting of the instance._

![EC2 — instance being started](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*bMytNipcV7vtUJZ6acuKKg.jpeg)![EC2 instance startup notification](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*zxlQv8wbEIwriDInS6BxAw.jpeg)

> _Stopping of the EC2 instance and getting notified about the Stopping of the instance._

![EC2 — instance being stopped](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*6TvHQrGn4YuCpQw6VyHpkg.jpeg)![EC2 instance stopped notification](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*OunKPoKJJciJI4EGRHrRqg.jpeg)

Conclusion
----------

By scheduling start and stop actions through cron expressions, the instance operates only when needed, optimizing cost and efficiency. SNS notifications ensure real-time alerts on each action. The project is simple, cost-effective, and a great example of using AWS services to automate cloud operations.
