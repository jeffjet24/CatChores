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
    print("Received event: " + json.dumps(event, indent=2))
    return respond(None, {"Message":"Thanks!"})