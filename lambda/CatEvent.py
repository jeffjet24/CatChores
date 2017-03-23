from __future__ import print_function

import boto3
import json
from datetime import datetime


tableName = "CatChores"
dynamodb = boto3.resource('dynamodb').Table('CatChores')
dynamodb.load()


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    actorName = ""
    time = ""
    eventName = ""
    if "Records" in event:
        snsMessage = json.loads(event["Records"][0]["Sns"]["Message"])
        actorName = snsMessage["name"]
        time = int(snsMessage["time"])
        eventName = snsMessage["event"]
    else:
        actorName = event["name"]
        time = int(event["time"])
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
    if "Records" not in event:
        return respond(response, "Thanks!")
    else:
        return 0
