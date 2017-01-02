from __future__ import print_function

import boto3
import json
from datetime import datetime


tableName = "CatChores"
dynamodb = boto3.resource('dynamodb').Table('CatChores')
dynamodb.load()

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


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

def getUser(given):
    if given == "mac":
        return "Mack"
    elif given == "autumn":
        return "Autumn"
    elif given == "david":
        return "David"
    elif given == "molly":
        return "Molly"
    elif given == "ben":
        return "Ben"
    elif given == "been":
        return "Ben"


def getActivity(given, cat):
    if given == "cleaned":
        return "DownstairLitter"
    elif given == "vacuumed":
        return "Vacuum"
    elif given == "vacuum":
        return "Vacuum"
    elif given == "emptied":
        return "DownstairLitter"
    elif given == "clipped":
        return cat + "Nails"
    elif given == "fed":
        # Add time determining logic...
        return "FeedAM"


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    if 'session' in event:
        eventName = ""
        actorName = getUser(event["request"]["intent"]["slots"]["User"]["value"])
        if "value" in event["request"]["intent"]["slots"]["Cat"]:
            catName = event["request"]["intent"]["slots"]["Cat"]["value"]
            eventName = getActivity(event["request"]["intent"]["slots"]["Chore"]["value"], catName)
        else:
            eventName = getActivity(event["request"]["intent"]["slots"]["Chore"]["value"], "")
        utc_dt = datetime.strptime(event["request"]["timestamp"], '%Y-%m-%dT%H:%M:%SZ')
        time = int((utc_dt - datetime(1970, 1, 1)).total_seconds())
        
        itemParams = {
            "time": time,
            "task": eventName,
            "personName": actorName
        }
        print("Params: " + json.dumps(itemParams, indent=2))
        response = dynamodb.put_item(
            Item = itemParams,
            ReturnConsumedCapacity = 'TOTAL'
        )
        if response == 200:
            speech_output = "Thank You! Have a nice day!"
            return build_response({}, build_speechlet_response("Cat Chores", speech_output, None, True))

    else:
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