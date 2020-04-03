# serverless invoke local --function functionName
import boto3
import datetime
import os
import json
import uuid

'''
Items: [{
    'active_cases': {
        'S': '74'
    },
    ...
},...]
'''

def getNumericalValues(item, propName, firstPrecedence, secondPrecedence):
    data = None
    try:
        data = item[propName][firstPrecedence]
    except Exception as exc:
        data = item[propName][secondPrecedence]
    return data

def normalize(item):
    return {
        'active_cases': getNumericalValues(item, 'active_cases', 'N', 'S'),
        'created_at': getNumericalValues(item, 'created_at', 'S', 'S'),
        'cases': getNumericalValues(item, 'cases', 'N', 'S'),
        'country': getNumericalValues(item, 'country', 'S', 'S'),
        'recovered': getNumericalValues(item, 'recovered', 'N', 'S'),
        'deaths': getNumericalValues(item, 'deaths', 'N', 'S'),
        'new_deaths': getNumericalValues(item, 'new_deaths', 'N', 'S'),
        'serious_critical': getNumericalValues(item, 'serious_critical', 'N', 'S'),
    }

def veoci_normalize_entries(item):
    return {
        'custom_0': getNumericalValues(item, 'country', 'S', 'S'),
        'custom_1': getNumericalValues(item, 'created_at', 'S', 'S'),
        'custom_2': getNumericalValues(item, 'cases', 'N', 'S'),
        'custom_3': getNumericalValues(item, 'active_cases', 'N', 'S'),
        'custom_4': getNumericalValues(item, 'recovered', 'N', 'S'),
        'custom_5': getNumericalValues(item, 'deaths', 'N', 'S'),
        'custom_6': getNumericalValues(item, 'new_deaths', 'N', 'S'),
        'custom_7': getNumericalValues(item, 'serious_critical', 'N', 'S'),
        'id': str(uuid.uuid4())
    }

def main(event, context):
    # Get todays date
    today = datetime.datetime.utcnow().date()
    # Code goes here
    # Add the data to dynamoDB table
    client = boto3.client('dynamodb')
    tableName = os.environ['tableName']
    # Query the items
    try:
        r = client.query(
                        TableName=tableName,
                        KeyConditionExpression='created_at = :created_at',
                        ExpressionAttributeValues={ ":created_at": { "S": str(today) } },
                    )
        data = r['Items']
        if len(data) == 0:
            yesterday = today - datetime.timedelta(days=1)
            # Get yesterday data
            r = client.query(
                        TableName=tableName,
                        KeyConditionExpression='created_at = :created_at',
                        ExpressionAttributeValues={ ":created_at": { "S": str(yesterday) } },
                    )
            data = r['Items']
        entries = list(map(veoci_normalize_entries, data))
        fields = []
        if len(entries) > 0:
            fields = [
                {
                    'name': 'country',
                    'type': 'TEXT',
                    'fieldId': str(uuid.uuid4()),
                    'index': 0
                },
                {
                    'name': 'created_at',
                    'type': 'DATE',
                    'fieldId': str(uuid.uuid4()),
                    'index': 1
                },
                {
                    'name': 'cases',
                    'type': 'NUMERIC',
                    'fieldId': str(uuid.uuid4()),
                    'index': 2
                },
                {
                    'name': 'active_cases',
                    'type': 'NUMERIC',
                    'fieldId': str(uuid.uuid4()),
                    'index': 3
                },
                {
                    'name': 'recovered',
                    'type': 'NUMERIC',
                    'fieldId': str(uuid.uuid4()),
                    'index': 4
                },
                {
                    'name': 'deaths',
                    'type': 'TEXT',
                    'fieldId': str(uuid.uuid4()),
                    'index': 5
                },
                {
                    'name': 'new_deaths',
                    'type': 'TEXT',
                    'fieldId': str(uuid.uuid4()),
                    'index': 6
                },
                {
                    'name': 'serious_critical',
                    'type': 'NUMERIC',
                    'fieldId': str(uuid.uuid4()),
                    'index': 7
                }
            ]
        return_data = {
            'entries': entries,
            'fields': fields
        }
        return {
            'statusCode': 200,
            'body': json.dumps(return_data)
        }
    except Exception as exc:
        print(exc)
        return {
            'statusCode': 400,
            'body': '{"status": "fail"}',
        }

if __name__ == "__main__":
    main('', '')