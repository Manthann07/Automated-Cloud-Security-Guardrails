import json
import boto3

s3 = boto3.client('s3')
ec2 = boto3.client('ec2')
sns = boto3.client('sns')

SNS_TOPIC_ARN = "arn:aws:sns:eu-north-1:809683733891:security-guardrail-alerts"

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))

    detail = event.get("detail", {})
    source = detail.get("eventSource")
    event_name = detail.get("eventName")

    # -------- S3 AUTO REMEDIATION --------
    if source == "s3.amazonaws.com":
        bucket_name = detail.get("requestParameters", {}).get("bucketName")
        if bucket_name:
            s3.put_public_access_block(
                Bucket=bucket_name,
                PublicAccessBlockConfiguration={
                    "BlockPublicAcls": True,
                    "IgnorePublicAcls": True,
                    "BlockPublicPolicy": True,
                    "RestrictPublicBuckets": True
                }
            )
            notify(f"S3 public access blocked for bucket: {bucket_name}")

    # -------- SECURITY GROUP AUTO REMEDIATION --------
    if source == "ec2.amazonaws.com" and event_name == "AuthorizeSecurityGroupIngress":
        sg_id = detail.get("requestParameters", {}).get("groupId")
        if sg_id:
            ec2.revoke_security_group_ingress(
                GroupId=sg_id,
                IpPermissions=[{
                    "IpProtocol": "tcp",
                    "FromPort": 22,
                    "ToPort": 22,
                    "IpRanges": [{"CidrIp": "0.0.0.0/0"}]
                }]
            )
            notify(f"Open SSH (22) removed from Security Group: {sg_id}")

    return {
        "statusCode": 200,
        "body": "Auto-remediation executed"
    }

def notify(message):
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject="Guardrail Auto-Remediation",
        Message=message
    )
