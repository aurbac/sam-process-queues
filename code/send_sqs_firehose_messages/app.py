import json
import os
import boto3
from botocore.exceptions import ClientError

sns = boto3.client('sns')
firehose = boto3.client('firehose')

def lambda_handler(event, context):

    TOPIC_ARN = os.environ['TOPIC_ARN']
    DELIVERY_STREAM_NAME = os.environ['DELIVERY_STREAM_NAME']
    
    print(json.dumps(event))
    
    messages = []
    
    
    try:
        for record in event['Records']:
            print(record)
            print("------")
            print(record['body'])
            print("------")
            print(record['messageAttributes'])
            response = sns.publish(
                TopicArn=TOPIC_ARN,
                Message=str(record['messageAttributes']),
                Subject=record['body']
            )
            messages.append({'Data': json.dumps({ 'Population': int(record['messageAttributes']['Population']['stringValue']), 'City': record['messageAttributes']['City']['stringValue'] }) })
            print(response)
            
        print("[[[[[[[[[[[[[")
        print(messages)
        
        response_firehose = firehose.put_record_batch(
            DeliveryStreamName=DELIVERY_STREAM_NAME,
            Records=messages
        )
        
        print(response_firehose)
            
    except Exception as e:
        print(e)
        raise e
            
    return True