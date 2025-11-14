import json
import boto3
import base64
from datetime import datetime
from decimal import Decimal

# Initialize AWS SDK clients
dynamodb = boto3.resource('dynamodb')

# DynamoDB tables
raw_events_table = dynamodb.Table('raw-events')
analytics_table = dynamodb.Table('analytics')


def process_record(record):
    """
    Process a single Kinesis record
    
    Args:
        record: Kinesis record from the event
        
    Returns:
        dict: Processed event data
    """
    # Decode the data (Kinesis encodes it in base64)
    payload = base64.b64decode(record['kinesis']['data'])
    event_data = json.loads(payload)
    
    return event_data


def save_raw_event(event_data):
    """
    Save raw event to DynamoDB raw-events table
    
    Args:
        event_data (dict): The event to save
    """
    try:
        # Convert float to Decimal (DynamoDB requirement)
        if 'product_price' in event_data:
            event_data['product_price'] = Decimal(str(event_data['product_price']))
        if 'total_amount' in event_data:
            event_data['total_amount'] = Decimal(str(event_data['total_amount']))
        
        # Save to DynamoDB
        raw_events_table.put_item(Item=event_data)
        print(f"✓ Saved raw event: {event_data['event_id']}")
        
    except Exception as e:
        print(f"✗ Error saving raw event: {str(e)}")
        raise


def update_analytics(event_data):
    """
    Update aggregated analytics in DynamoDB analytics table
    
    Args:
        event_data (dict): The event to aggregate
    """
    try:
        # Get date from timestamp
        timestamp = event_data['timestamp']
        date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        
        event_type = event_data['event_type']
        
        # Update count for this event type on this date
        metric_type = f"{event_type}_count"
        time_window = date
        
        # Increment the counter (atomic operation)
        analytics_table.update_item(
            Key={
                'metric_type': metric_type,
                'time_window': time_window
            },
            UpdateExpression='ADD event_count :inc SET last_updated = :now',
            ExpressionAttributeValues={
                ':inc': 1,
                ':now': int(datetime.now().timestamp())
            }
        )
        
        print(f"✓ Updated analytics: {metric_type} for {time_window}")
        
        # If it's a purchase, also track revenue
        if event_type == 'purchase' and 'total_amount' in event_data:
            revenue_metric = 'purchase_revenue'
            analytics_table.update_item(
                Key={
                    'metric_type': revenue_metric,
                    'time_window': time_window
                },
                UpdateExpression='ADD total_revenue :amount SET last_updated = :now',
                ExpressionAttributeValues={
                    ':amount': Decimal(str(event_data['total_amount'])),
                    ':now': int(datetime.now().timestamp())
                }
            )
            print(f"✓ Updated revenue: ${event_data['total_amount']} for {time_window}")
        
    except Exception as e:
        print(f"✗ Error updating analytics: {str(e)}")
        raise


def lambda_handler(event, context):
    """
    Main Lambda handler - triggered by Kinesis
    
    Args:
        event: Kinesis event with records
        context: Lambda context
        
    Returns:
        dict: Processing results
    """
    print(f"Stream Processor Lambda started - processing {len(event['Records'])} records")
    
    successful = 0
    failed = 0
    
    # Process each record from Kinesis
    for record in event['Records']:
        try:
            # Decode and parse the event
            event_data = process_record(record)
            
            print(f"Processing: {event_data['event_type']} - {event_data['product_name']}")
            
            # Save to raw events table
            save_raw_event(event_data)
            
            # Update aggregated analytics
            update_analytics(event_data)
            
            successful += 1
            
        except Exception as e:
            print(f"✗ Failed to process record: {str(e)}")
            failed += 1
    
    print(f"Stream Processor completed: {successful} successful, {failed} failed")
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'processed': successful,
            'failed': failed
        })
    }