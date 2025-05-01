import json
import boto3
import uuid
from datetime import datetime, timedelta
import os
import logging
from decimal import Decimal

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('digital-chitthi-letters')

# Custom JSON encoder to handle Decimal
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)

def create_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body, cls=DecimalEncoder)
    }

def lambda_handler(event, context):
    logger.info('Event received: %s', event)
    
    # Handle OPTIONS request for CORS
    http_method = event.get('httpMethod') or event.get('requestContext', {}).get('http', {}).get('method')
    logger.info('HTTP Method: %s', http_method)
    
    if http_method == 'OPTIONS':
        return create_response(200, {'message': 'CORS enabled'})
    
    try:
        if http_method == 'POST':
            return handle_post_request(event)
        elif http_method == 'GET':
            return handle_get_request(event)
        else:
            logger.error('Invalid HTTP method: %s', http_method)
            return create_response(405, {'error': f'Method not allowed: {http_method}'})
    except Exception as e:
        logger.error('Error processing request: %s', str(e), exc_info=True)
        return create_response(500, {'error': str(e)})

def handle_post_request(event):
    try:
        # Parse the request body
        body = event.get('body', '{}')
        if isinstance(body, str):
            body = json.loads(body)
        logger.info('Received POST body: %s', body)
        
        # Validate required fields
        if 'receiver' not in body or 'content' not in body:
            return create_response(400, {'error': 'Missing required fields'})
        
        # Generate a unique ID for the letter
        letter_id = str(uuid.uuid4())
        
        # Calculate expiry date
        expiry_days = body.get('expiryDays', '7')
        expiry_date = None
        if expiry_days != 'never':
            try:
                days = int(expiry_days)
                expiry_date = (datetime.now() + timedelta(days=days)).isoformat()
            except ValueError:
                return create_response(400, {'error': 'Invalid expiry days'})
        
        # Prepare the letter item
        letter_item = {
            'letter_id': letter_id,
            'sender': body.get('sender', 'Anonymous'),
            'receiver': body['receiver'],
            'content': body['content'],
            'is_anonymous': body.get('isAnonymous', False),
            'is_public': body.get('isPublic', False),
            'created_at': datetime.now().isoformat(),
            'expiry_date': expiry_date,
            'views': 0
        }
        
        logger.info('Saving letter: %s', letter_item)
        
        # Save to DynamoDB
        table.put_item(Item=letter_item)
        
        # Generate the letter URL
        base_url = 'digital-chitthi-web.s3-website-us-east-1.amazonaws.com'
        letter_url = f"http://{base_url}/letter/{letter_id}"
        
        return create_response(200, {
            'success': True,
            'letterUrl': letter_url,
            'letter_id': letter_id
        })
        
    except Exception as e:
        logger.error('Error in handle_post_request: %s', str(e), exc_info=True)
        return create_response(500, {'error': f'Failed to save letter: {str(e)}'})

def handle_get_request(event):
    try:
        # Extract letter ID from path parameters
        path_parameters = event.get('pathParameters', {})
        logger.info('Path parameters: %s', path_parameters)
        
        if not path_parameters or 'letter_id' not in path_parameters:
            return create_response(400, {'error': 'Missing letter ID'})
            
        letter_id = path_parameters['letter_id']
        logger.info('Getting letter: %s', letter_id)
        
        # Get letter from DynamoDB
        response = table.get_item(Key={'letter_id': letter_id})
        
        if 'Item' not in response:
            return create_response(404, {'error': 'Letter not found'})
        
        letter = response['Item']
        
        # Check if letter has expired
        if letter.get('expiry_date'):
            expiry_date = datetime.fromisoformat(letter['expiry_date'])
            if expiry_date < datetime.now():
                # Delete expired letter
                table.delete_item(Key={'letter_id': letter_id})
                return create_response(404, {'error': 'Letter has expired'})
        
        # Increment view count using expression attribute names to handle reserved keyword
        try:
            update_response = table.update_item(
                Key={'letter_id': letter_id},
                UpdateExpression='SET #v = if_not_exists(#v, :start) + :inc',
                ExpressionAttributeNames={'#v': 'views'},
                ExpressionAttributeValues={':inc': 1, ':start': 0},
                ReturnValues='UPDATED_NEW'
            )
            current_views = int(update_response.get('Attributes', {}).get('views', 1))
        except Exception as e:
            logger.error('Error updating view count: %s', str(e))
            current_views = int(letter.get('views', 0)) + 1
        
        # Return letter data
        return create_response(200, {
            'success': True,
            'letter': {
                'sender': letter['sender'],
                'receiver': letter['receiver'],
                'content': letter['content'],
                'created_at': letter['created_at'],
                'views': current_views
            }
        })
    except Exception as e:
        logger.error('Error in handle_get_request: %s', str(e), exc_info=True)
        return create_response(500, {'error': f'Failed to retrieve letter: {str(e)}'})
