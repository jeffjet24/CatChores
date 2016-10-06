from __future__ import print_function
from operator import itemgetter

import boto3
import json
import datetime
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

def getFoodStatus(lastTime):
    return {"status":"yellow", "item": lastTime}
    # return {status: statusVal, item: lastTime}

def getLitterStatus(lastTime):
    return {"status":"green", "item": lastTime}
    # return {status: statusVal, item: lastTime}

def getMonthlyStatus(lastTime):
    return {"status":"red", "item": lastTime}
    # return {status: statusVal, item: lastTime}

def sortingLayer(item):
    if item is not None:
        taskType = str(item["task"])
        if taskType == "FeedAM" or taskType == "FeedPM":
            return getFoodStatus(item)
        elif taskType == "DownstairLitter" or taskType == "UpstairLitter":
            return getLitterStatus(item)
        elif taskType == "Vacuum" or taskType == "MillieNails" or taskType == "KittyXNails":
            return getMonthlyStatus(item)
        else:
            return {"status":"mustBeNope", "item": item}
    else:
        return {"status":"mustBeNone", "item": item}



def lambda_handler(event, context):
    # I am doing NO checking for nonexisting items... so.... yeah... 

    results = {
        "feedAMList":[],
        "feedPMList":[],
        "upstairsList":[],
        "downstairsList":[],
        "vacuumList":[],
        "millieNailsList":[],
        "kittyXNailsList":[]
    }
    

    print("Received event: " + json.dumps(event, indent=2))
    response = dynamodb.scan(
        TableName = tableName,
        Select = "ALL_ATTRIBUTES"
    )

    print("DynamoDB Response:" + str(response))
    for item in response["Items"]:
        taskType = item["task"]
        # This is going to get real ugly.. but they don't have switch statements in python... and mapping it to a dict is not ideal...
        if taskType == "FeedAM":
            results["feedAMList"].append(item)
        elif taskType == "FeedPM":
            results["feedPMList"].append(item)
        elif taskType == "DownstairLitter":
            results["downstairsList"].append(item)
        elif taskType == "UpstairLitter":
            results["upstairsList"].append(item)
        elif taskType == "Vacuum":
            results["vacuumList"].append(item)
        elif taskType == "MillieNails":
            results["millieNailsList"].append(item)
        elif taskType == "KittyXNails":
            results["kittyXNailsList"].append(item)

    resultList = []
    for key, value in results.iteritems():
        # sort the values in ascending order by timestamp
        sorted(results[key], key=itemgetter('time'))
        # grab the one with the highest timestamp
        resultList.append(sortingLayer(results[key].pop()))


    print("The End Results are: " + str(resultList))
    return respond(None, {"Message":"Thanks!"})