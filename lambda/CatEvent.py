from __future__ import print_function

import boto3
import json
from datetime import datetime


tableName = "CatChores"
dynamodb = boto3.resource('dynamodb').Table('CatChores')
dynamodb.load()


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    #     eventName = ""
    #     actorName = getUser(event["request"]["intent"]["slots"]["User"]["value"])
    #     if "value" in event["request"]["intent"]["slots"]["Cat"]:
    #         catName = event["request"]["intent"]["slots"]["Cat"]["value"]
    #         eventName = getActivity(event["request"]["intent"]["slots"]["Chore"]["value"], catName)
    #     else:
    #         eventName = getActivity(event["request"]["intent"]["slots"]["Chore"]["value"], "")
    #     utc_dt = datetime.strptime(event["request"]["timestamp"], '%Y-%m-%dT%H:%M:%SZ')
    #     time = int((utc_dt - datetime(1970, 1, 1)).total_seconds())
    #
    #     itemParams = {
    #         "time": time,
    #         "task": eventName,
    #         "personName": actorName
    #     }
    #     print("Params: " + json.dumps(itemParams, indent=2))
    #     response = dynamodb.put_item(
    #         Item = itemParams,
    #         ReturnConsumedCapacity = 'TOTAL'
    #     )
    #     if response == 200:
    #         speech_output = "Thank You! Have a nice day!"
    #         return build_response({}, build_speechlet_response("Cat Chores", speech_output, None, True))
    #
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
