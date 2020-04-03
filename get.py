# serverless invoke local --function functionName
import boto3
import datetime
import os
import json

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
        return_data = list(map(normalize, data))
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