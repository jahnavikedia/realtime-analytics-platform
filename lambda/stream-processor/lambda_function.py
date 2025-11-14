import json
import boto3
import base64
import time
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


def update_metric(metric_type, time_window, increment):
    """
    Update or create a metric in the analytics table
    
    Args:
        metric_type (str): Type of metric (e.g., "product_view_count", "category_Electronics")
        time_window (str): Time period (e.g., "2025-11-14" or "2025-11-14-14")
        increment (float): Amount to add to the metric
    """
    try:
        # Convert to Decimal for DynamoDB
        increment_decimal = Decimal(str(increment))
        
        # Use DynamoDB's atomic counter
        # If item doesn't exist, it creates it with event_count=increment
        # If item exists, it adds increment to existing event_count
        analytics_table.update_item(
            Key={
                'metric_type': metric_type,
                'time_window': time_window
            },
            UpdateExpression='ADD event_count :increment SET last_updated = :timestamp',
            ExpressionAttributeValues={
                ':increment': increment_decimal,
                ':timestamp': Decimal(str(int(time.time())))
            }
        )
        
    except Exception as e:
        print(f"✗ Error updating metric {metric_type}/{time_window}: {str(e)}")
        raise


def update_analytics(event):
    """
    Update aggregated analytics in DynamoDB
    
    Args:
        event (dict): Event data to aggregate
    """
    try:
        # Get date for time window (YYYY-MM-DD format)
        event_date = datetime.fromtimestamp(event['timestamp']).strftime('%Y-%m-%d')
        
        # Get hour for hourly metrics (YYYY-MM-DD-HH format)
        event_hour = datetime.fromtimestamp(event['timestamp']).strftime('%Y-%m-%d-%H')
        
        # Get event type (e.g., "product_view", "add_to_cart")
        event_type = event['event_type']
        
        # Update daily event type counter
        update_metric(
            metric_type=f"{event_type}_count",
            time_window=event_date,
            increment=1
        )
        
        # Update hourly event type counter
        update_metric(
            metric_type=f"{event_type}_hourly_count",
            time_window=event_hour,
            increment=1
        )
        
        # Update category metrics (daily)
        category = event.get('product_category')
        if category:
            update_metric(
                metric_type=f"category_{category}",
                time_window=event_date,
                increment=1
            )
        
        # Update product-specific metrics (daily)
        product_id = event.get('product_id')
        if product_id:
            update_metric(
                metric_type=f"product_{product_id}",
                time_window=event_date,
                increment=1
            )
        
        # If it's a purchase, track revenue
        if event_type == 'purchase':
            revenue = event.get('total_amount', event.get('product_price', 0))
            update_metric(
                metric_type='purchase_revenue',
                time_window=event_date,
                increment=float(revenue)
            )
        
        print(f"✓ Updated analytics for: {event_type} - {event.get('product_name')}")
        
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