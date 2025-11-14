import json
import boto3
from decimal import Decimal
from datetime import datetime, timedelta

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb')
analytics_table = dynamodb.Table('analytics')
raw_events_table = dynamodb.Table('raw-events')


class DecimalEncoder(json.JSONEncoder):
    """
    Helper class to convert Decimal to float for JSON serialization
    DynamoDB returns numbers as Decimal, but JSON doesn't support Decimal
    """
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)


def get_metric(metric_type, time_window=None):
    """
    Get a specific metric from analytics table
    
    Args:
        metric_type (str): Type of metric (e.g., "product_view", "purchase")
        time_window (str): Optional specific date (e.g., "2025-11-14")
        
    Returns:
        dict: Metric data or list of metrics
    """
    try:
        if time_window:
            # Query specific date
            response = analytics_table.get_item(
                Key={
                    'metric_type': metric_type,
                    'time_window': time_window
                }
            )
            
            if 'Item' in response:
                return {
                    'success': True,
                    'data': response['Item']
                }
            else:
                return {
                    'success': False,
                    'message': f'No data found for {metric_type} on {time_window}'
                }
        else:
            # Query all time windows for this metric
            response = analytics_table.query(
                KeyConditionExpression='metric_type = :mt',
                ExpressionAttributeValues={
                    ':mt': metric_type
                },
                Limit=30  # Last 30 days max
            )
            
            return {
                'success': True,
                'data': response['Items'],
                'count': len(response['Items'])
            }
            
    except Exception as e:
        print(f"Error querying metric: {str(e)}")
        return {
            'success': False,
            'message': f'Error: {str(e)}'
        }


def get_dashboard_summary():
    """
    Get summary of key metrics for today
    
    Returns:
        dict: Summary of all key metrics
    """
    try:
        # Get today's date
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Key metrics to fetch
        metrics = ['product_view_count', 'add_to_cart_count', 'purchase_count', 'remove_from_cart_count']
        
        summary = {
            'date': today,
            'metrics': {}
        }
        
        # Fetch each metric
        for metric in metrics:
            result = get_metric(metric, today)
            if result['success'] and 'data' in result:
            # Remove "_count" suffix for cleaner response
                clean_name = metric.replace('_count', '')
                summary['metrics'][clean_name] = result['data'].get('event_count', 0)
            else:
                clean_name = metric.replace('_count', '')
                summary['metrics'][clean_name] = 0
        
        # Calculate conversion rate (purchases / views)
        views = summary['metrics'].get('product_view', 0)
        purchases = summary['metrics'].get('purchase', 0)
        
        if views > 0:
            summary['conversion_rate'] = round((purchases / views) * 100, 2)
        else:
            summary['conversion_rate'] = 0
        
        # Calculate cart abandonment (add_to_cart - purchase) / add_to_cart
        cart_adds = summary['metrics'].get('add_to_cart', 0)
        if cart_adds > 0:
            summary['cart_abandonment_rate'] = round(((cart_adds - purchases) / cart_adds) * 100, 2)
        else:
            summary['cart_abandonment_rate'] = 0
        
        return {
            'success': True,
            'data': summary
        }
        
    except Exception as e:
        print(f"Error getting dashboard summary: {str(e)}")
        return {
            'success': False,
            'message': f'Error: {str(e)}'
        }


def get_category_breakdown(date=None):
    """
    Get breakdown of views by category
    
    Args:
        date (str): Optional specific date
        
    Returns:
        dict: Category metrics
    """
    try:
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        categories = ['Electronics', 'Sports', 'Home']
        breakdown = {
            'date': date,
            'categories': {}
        }
        
        for category in categories:
            metric_type = f'category_{category}'
            
            # Get the metric data
            response = analytics_table.get_item(
                Key={
                    'metric_type': metric_type,
                    'time_window': date
                }
            )
            
            # Extract the count
            if 'Item' in response:
                breakdown['categories'][category] = float(response['Item'].get('event_count', 0))
            else:
                breakdown['categories'][category] = 0
        
        return {
            'success': True,
            'data': breakdown
        }
        
    except Exception as e:
        print(f"Error getting category breakdown: {str(e)}")
        return {
            'success': False,
            'message': f'Error: {str(e)}'
        }


def lambda_handler(event, context):
    """
    Main Lambda handler for API requests
    
    Args:
        event: API Gateway event
        context: Lambda context
        
    Returns:
        dict: API Gateway response
    """
    print(f"Received event: {json.dumps(event)}")
    
    # Extract path and parameters
    path = event.get('path', '')
    method = event.get('httpMethod', 'GET')
    path_parameters = event.get('pathParameters', {})
    query_parameters = event.get('queryStringParameters', {}) or {}
    
    try:
        # Route requests
        if path == '/dashboard/summary':
            result = get_dashboard_summary()
            
        elif path == '/dashboard/categories':
            date = query_parameters.get('date')
            result = get_category_breakdown(date)
            
        elif path.startswith('/metrics/'):
            metric_type = path_parameters.get('metric_type')
            date = path_parameters.get('date')
            
            if not metric_type:
                result = {
                    'success': False,
                    'message': 'metric_type is required'
                }
            else:
                result = get_metric(metric_type, date)
        else:
            result = {
                'success': False,
                'message': 'Invalid endpoint'
            }
        
        # Return response
        return {
            'statusCode': 200 if result['success'] else 404,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'  # CORS for web apps
            },
            'body': json.dumps(result, cls=DecimalEncoder)
        }
        
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'success': False,
                'message': f'Internal error: {str(e)}'
            })
        }