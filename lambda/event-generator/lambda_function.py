import json
import boto3
import random
import time
from datetime import datetime
import uuid

# Initialize AWS SDK clients
# boto3 = AWS SDK for Python (lets Python talk to AWS services)
kinesis_client = boto3.client('kinesis')

# Configuration
STREAM_NAME = 'ecommerce-events'  # The Kinesis stream we created

# Simulate realistic e-commerce data
PRODUCTS = [
    {'id': 'prod_001', 'name': 'Wireless Headphones', 'price': 79.99, 'category': 'Electronics'},
    {'id': 'prod_002', 'name': 'Running Shoes', 'price': 120.00, 'category': 'Sports'},
    {'id': 'prod_003', 'name': 'Coffee Maker', 'price': 45.50, 'category': 'Home'},
    {'id': 'prod_004', 'name': 'Yoga Mat', 'price': 25.99, 'category': 'Sports'},
    {'id': 'prod_005', 'name': 'Laptop Stand', 'price': 35.00, 'category': 'Electronics'},
    {'id': 'prod_006', 'name': 'Water Bottle', 'price': 18.99, 'category': 'Sports'},
    {'id': 'prod_007', 'name': 'Desk Lamp', 'price': 32.50, 'category': 'Home'},
    {'id': 'prod_008', 'name': 'Bluetooth Speaker', 'price': 55.00, 'category': 'Electronics'},
]

EVENT_TYPES = [
    'product_view',
    'add_to_cart',
    'purchase',
    'remove_from_cart',
]

# Weighted random selection - makes data realistic
# 70% views, 20% cart adds, 8% purchases, 2% removals
EVENT_WEIGHTS = [70, 20, 8, 2]


def generate_event():
    """
    Generate a single realistic e-commerce event
    
    Returns:
        dict: Event data with all necessary fields
    """
    # Pick a random product
    product = random.choice(PRODUCTS)
    
    # Pick an event type (weighted - more views than purchases)
    event_type = random.choices(EVENT_TYPES, weights=EVENT_WEIGHTS)[0]
    
    # Generate a realistic user ID (simulate 1000 active users)
    user_id = f"user_{random.randint(1, 1000):04d}"
    
    # Create the event
    event = {
        'event_id': str(uuid.uuid4()),  # Unique ID for this event
        'event_type': event_type,
        'user_id': user_id,
        'product_id': product['id'],
        'product_name': product['name'],
        'product_price': product['price'],
        'product_category': product['category'],
        'timestamp': int(time.time()),  # Unix timestamp (seconds since 1970)
        'session_id': f"session_{random.randint(1, 500):04d}",
    }
    
    # Add extra fields for purchase events
    if event_type == 'purchase':
        event['quantity'] = random.randint(1, 3)
        event['total_amount'] = round(product['price'] * event['quantity'], 2)
    
    return event


def send_to_kinesis(event):
    """
    Send an event to Kinesis Data Stream
    
    Args:
        event (dict): The event to send
        
    Returns:
        dict: Response from Kinesis
    """
    try:
        response = kinesis_client.put_record(
            StreamName=STREAM_NAME,
            Data=json.dumps(event),  # Convert Python dict to JSON string
            PartitionKey=event['user_id']  # Events from same user go to same shard
        )
        return response
    except Exception as e:
        print(f"Error sending to Kinesis: {str(e)}")
        raise


def lambda_handler(event, context):
    """
    Main Lambda function handler - AWS calls this function
    
    Args:
        event: Event data from Lambda trigger
        context: Runtime information from Lambda
        
    Returns:
        dict: Response with status and results
    """
    print("Event Generator Lambda started")
    
    # Generate multiple events (simulate traffic burst)
    num_events = 10
    
    successful_events = 0
    failed_events = 0
    
    for i in range(num_events):
        try:
            # Generate one event
            event_data = generate_event()
            
            # Send it to Kinesis
            response = send_to_kinesis(event_data)
            
            # Log success
            print(f"✓ Event {i+1}/{num_events} sent: {event_data['event_type']} - {event_data['product_name']}")
            successful_events += 1
            
        except Exception as e:
            print(f"✗ Event {i+1}/{num_events} failed: {str(e)}")
            failed_events += 1
    
    # Return summary
    result = {
        'statusCode': 200,
        'body': json.dumps({
            'message': f'Generated {num_events} events',
            'successful': successful_events,
            'failed': failed_events,
            'timestamp': datetime.now().isoformat()
        })
    }
    
    print(f"Event Generator completed: {successful_events} successful, {failed_events} failed")
    return result