"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
from urllib.parse import urlencode
from urllib.request import Request, urlopen

catEventEndpoint = 'https://5vsoxh69gj.execute-api.us-east-1.amazonaws.com/v1/cat-event' # Set destination URL here





from operator import itemgetter

import boto3
import json
from datetime import tzinfo, timedelta, datetime

# --------------- Helpers that build all of the responses ----------------------

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

# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Cat Chores Alexa Skill!" \
                    "Please tell me what chore has been just been completed. "\
                    "Please say it in past tense."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me what chore has been just been completed. "\
                    "Please say it in past tense."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you! Have a nice day!"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_favorite_color_attributes(favorite_color):
    return {"favoriteColor": favorite_color}


def performChore(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False


    eventName = ""
    actorName = getUser(event["request"]["intent"]["slots"]["User"]["value"])
    if "value" in event["request"]["intent"]["slots"]["Cat"]:
        catName = event["request"]["intent"]["slots"]["Cat"]["value"]
        eventName = getActivity(event["request"]["intent"]["slots"]["Chore"]["value"], catName)
    else:
        eventName = getActivity(event["request"]["intent"]["slots"]["Chore"]["value"], "")
    utc_dt = datetime.strptime(event["request"]["timestamp"], '%Y-%m-%dT%H:%M:%SZ')
    time = int((utc_dt - datetime(1970, 1, 1)).total_seconds())


    post_message = {'name': actorName, "time": time, "event": eventName}
    request = Request(catEventEndpoint, urlencode(post_message).encode())
    json = urlopen(request).read().decode()
    print(json)

    speech_output = "Thank You! That record has been added!"
    reprompt_text = "Please tell me what chore has been just been completed. "\
                    "Please say it in past tense."
    session_attributes = {}

    # if 'Color' in intent['slots']:
    #     favorite_color = intent['slots']['Color']['value']
    #     session_attributes = create_favorite_color_attributes(favorite_color)
    #     speech_output = "I now know your favorite color is " + \
    #                     favorite_color + \
    #                     ". You can ask me your favorite color by saying, " \
    #                     "what's my favorite color?"
    #     reprompt_text = "You can ask me your favorite color by saying, " \
    #                     "what's my favorite color?"
    # else:
    #     speech_output = "I'm not sure what your favorite color is. " \
    #                     "Please try again."
    #     reprompt_text = "I'm not sure what your favorite color is. " \
    #                     "You can tell me your favorite color by saying, " \
    #                     "my favorite color is red."


    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_color_from_session(intent, session):
    session_attributes = {}
    reprompt_text = None

    if session.get('attributes', {}) and "favoriteColor" in session.get('attributes', {}):
        favorite_color = session['attributes']['favoriteColor']
        speech_output = "Your favorite color is " + favorite_color + \
                        ". Goodbye."
        should_end_session = True
    else:
        speech_output = "I'm not sure what your favorite color is. " \
                        "You can say, my favorite color is red."
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "PerformChore":
        return set_color_in_session(intent, session)
    elif intent_name == "QueryChore":
        return get_color_from_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])
    print("Received event: " + json.dumps(event, indent=2))
    

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
