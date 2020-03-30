# serverless invoke local --function functionName
import boto3
import datetime
import os

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
        body = { 'data': data, 'date': 'today' }
        if len(data) == 0:
            yesterday = today - datetime.timedelta(days=1)
            # Get yesterday data
            r = client.query(
                        TableName=tableName,
                        KeyConditionExpression='created_at = :created_at',
                        ExpressionAttributeValues={ ":created_at": { "S": str(yesterday) } },
                    )
            data = r['Items']
            body = { 'data': data, 'date': 'yesterday' }
        return {
            'statusCode': 200,
            'body': body
        }
    except Exception as exc:
        print(exc)
        return {
            'statusCode': 400,
            'body': '{"status": "fail"}',
        }

if __name__ == "__main__":
    main('', '')