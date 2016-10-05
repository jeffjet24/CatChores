from __future__ import print_function

import boto3
import json
tableName = "CatChores"
print('Loading function')
dynamodb = boto3.resource('dynamodb').Table('CatChores')
dynamodb.load()

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):
    feedAMList = []
    feedPMList = []
    upstairsList = []
    downstairsList = []
    vacuumList = []
    millieNailsList = []
    kittyXNailsList = []

    print("Received event: " + json.dumps(event, indent=2))
    response = dynamodb.scan(
        TableName = tableName,
        Select = "ALL_ATTRIBUTES"
    )

    for item in response["Items"]:
        taskType = item["task"]
        # This is going to get real ugly.. but they don't have switch statements in python... and mapping it to a dict is not ideal...
        if taskType == "FeedAM":
            feedAMList.append(item)
        else if taskType == "FeedPM":
            feedPMList.append(item)
        else if taskType == "DownstairLitter":
            downstairsList.append(item)
        else if taskType == "UpstairLitter":
            upstairsList.append(item)
        else if taskType == "Vacuum":
            vacuumList.append(item)
        else if taskType == "MillieNails":
            millieNailsList.append(item)
        else if taskType == "KittyXNails":
            kittyXNailsList.append(item)


    # insert code to sort by timestamp for each list


    return respond(None, {"Message":"Thanks!"})