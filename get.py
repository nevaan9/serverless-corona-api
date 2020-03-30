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
        response = client.query(
                        TableName=tableName,
                        KeyConditionExpression='created_at = :created_at',
                        ExpressionAttributeValues={ ":created_at": { "S": today } },
                    )
        data = response['Items']
        return {
            'statusCode': 200,
            'body': data,
        }
    except Exception as exc:
        print(exc)
        return {
            'statusCode': 400,
            'body': '{"status": "fail"}',
        }

if __name__ == "__main__":
    main('', '')