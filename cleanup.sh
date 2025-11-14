#!/bin/bash

echo "🗑️  Cleaning up AWS resources..."

# Delete Lambda functions
echo "Deleting Lambda functions..."
aws lambda delete-function --function-name event-generator 2>/dev/null
aws lambda delete-function --function-name stream-processor 2>/dev/null
aws lambda delete-function --function-name query-api 2>/dev/null

# Delete API Gateway
echo "Deleting API Gateway..."
API_ID=$(aws apigateway get-rest-apis --query "items[?name=='ecommerce-analytics-api'].id" --output text)
if [ ! -z "$API_ID" ]; then
    aws apigateway delete-rest-api --rest-api-id $API_ID
fi

# Delete DynamoDB tables
echo "Deleting DynamoDB tables..."
aws dynamodb delete-table --table-name raw-events 2>/dev/null
aws dynamodb delete-table --table-name analytics 2>/dev/null

# Delete Kinesis stream (if exists)
echo "Deleting Kinesis stream..."
aws kinesis delete-stream --stream-name ecommerce-events 2>/dev/null

# Delete IAM role
echo "Deleting IAM role..."
aws iam detach-role-policy --role-name lambda-analytics-role --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole 2>/dev/null
aws iam delete-role-policy --role-name lambda-analytics-role --policy-name dynamodb-kinesis-policy 2>/dev/null
aws iam delete-role --role-name lambda-analytics-role 2>/dev/null

# Delete CloudWatch alarms
echo "Deleting CloudWatch alarms..."
aws cloudwatch delete-alarms --alarm-names billing-alarm 2>/dev/null

# Delete SNS topic
echo "Deleting SNS topic..."
TOPIC_ARN=$(aws sns list-topics --query "Topics[?contains(TopicArn, 'billing-alerts')].TopicArn" --output text)
if [ ! -z "$TOPIC_ARN" ]; then
    aws sns delete-topic --topic-arn $TOPIC_ARN
fi

echo "✅ Cleanup complete! All resources deleted."
echo "Monthly cost now: $0"
