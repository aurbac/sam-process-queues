import json
import os
import boto3
from botocore.exceptions import ClientError

ecs = boto3.client('ecs')

def lambda_handler(event, context):

    CLUSTER_NAME = os.environ['CLUSTER_NAME']
    TASK_DEFINITION = os.environ['TASK_DEFINITION']
    TASK_ROLE_ARN = os.environ['TASK_ROLE_ARN']
    SUBNET_ID_01 = os.environ['SUBNET_ID_01']
    SUBNET_ID_02 = os.environ['SUBNET_ID_02']
    SECURITY_GROUP_ID = os.environ['SECURITY_GROUP_ID']
    QUEUE_URL = os.environ['QUEUE_URL']

    try:
        
        print(CLUSTER_NAME)
        
        response = ecs.run_task(
            cluster=CLUSTER_NAME,
            launchType='FARGATE',
            taskDefinition=TASK_DEFINITION.split('/')[1],
            overrides={
                'containerOverrides': [
                    {   'name': 'container', 
                        'environment': [
                            { 'name': 'QUEUE_URL', 'value': QUEUE_URL }
                        ] 
                    
                    }
                ],
                'taskRoleArn':TASK_ROLE_ARN,
#                    'ephemeralStorage': {
#                        'sizeInGiB': 50
#                    }
            },
            networkConfiguration={
                'awsvpcConfiguration': {
                            'subnets': [
                                SUBNET_ID_01,SUBNET_ID_02
                            ],
                            'securityGroups': [
                                SECURITY_GROUP_ID
                            ],
                            'assignPublicIp': 'ENABLED'
                        }
            }
        )
            
        return True
    except Exception as e:
        print(e)
        raise e