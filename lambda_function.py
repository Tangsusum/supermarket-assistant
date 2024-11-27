import json
from assistant import assistant

def lambda_handler(event, context):
    meta_data = {
        'headers': {
            "Access-Control-Allow-Origin": "*"
        },
    }

    user = event.get('queryStringParameters',{}).get('user', None)

    if None in [user]:
        return {
            **meta_data,
            'statusCode': 400,
            'body': 'Missing data in body'
        }
    
    response = assistant(user)

    return {
        **meta_data,
        'statusCode': 200,
        'body': json.dumps(response)
    }

    
