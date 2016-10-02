from __future__ import print_function

import boto3
import json
tableName = "CatChores"
print('Loading function')
dynamodb = boto3.resource('dynamodb').Table('CatChores')
dynamodb.load()

def respond(res, message=None):
    statusCode = res["ResponseMetadata"]["HTTPStatusCode"]
    err = int(statusCode) != 200
    return {
        'statusCode': statusCode if err else '200',
        'body': statusCode if err else json.dumps(message),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    actorName = event["name"]
    time = event["time"]
    eventName = event["event"]
    itemParams = {
        "time": time,
        "task": eventName,
        "personName": actorName
    }
    response = dynamodb.put_item(
        Item = itemParams,
        ReturnConsumedCapacity = 'TOTAL'
    )
    print("The Response was: " + str(response))
    return respond(response, "Thanks!")