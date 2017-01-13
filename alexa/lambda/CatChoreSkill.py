from operator import itemgetter
import boto3
import json
from datetime import tzinfo, timedelta, datetime

snsClient = boto3.client('sns')
lambdaClient = boto3.client('lambda')
catEventSNS = "arn:aws:sns:us-east-1:818316582971:CatEvent"
catGetPerformedLambda = "arn:aws:lambda:us-east-1:818316582971:function:CatGetPerformed"
TIMEZONE_DIFFERENCE = timedelta(hours = -6)
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


def build_response(sessionAttributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': sessionAttributes,
        'response': speechlet_response
    }


def getUser(given):
    given = given.lower()
    if given == "mac" or given == "mack":
        return "Mack"
    elif given == "autumn":
        return "Autumn"
    elif given == "david":
        return "David"
    elif given == "molly":
        return "Molly"
    elif given == "ben" or given == "been":
        return "Ben"


def getActivity(given, cat):
    given = given.lower()
    if given == "cleaned":
        return "DownstairLitter"
    elif given == "vacuumed" or given == "vacuum":
        return "Vacuum"
    elif given == "emptied" or given == "empty":
        return "DownstairLitter"
    elif given == "clipped":
        if cat == "millies" or cat == "millie" or cat == "milly":
            cat = "Millie"
        return cat + "Nails"
    elif given == "fed":
        # Add time (AM/PM) determining logic...
        return "FeedAM"

# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():

    card_title = "Welcome"
    speech_output = "Welcome to the Cat Chores Alexa Skill!" \
                    "Please tell me what chore has been just been completed and who has completed it. "\
                    "Please say it in past tense."\
                    " You can also ask when a chore has last been done "
    reprompt_text = "Please tell me what chore has been just been completed. "\
                    "Please say it in past tense."
    should_end_session = False
    return build_response({}, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you! Have a nice day!"
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def performChore(intent, session, event):
    card_title = intent['name']
    should_end_session = True

    eventName = ""
    actorName = getUser(event["request"]["intent"]["slots"]["User"]["value"])
    if "value" in event["request"]["intent"]["slots"]["Cat"]:
        catName = event["request"]["intent"]["slots"]["Cat"]["value"]
        eventName = getActivity(event["request"]["intent"]["slots"]["Chore"]["value"], catName)
    else:
        eventName = getActivity(event["request"]["intent"]["slots"]["Chore"]["value"], "")
    utc_dt = datetime.strptime(event["request"]["timestamp"], '%Y-%m-%dT%H:%M:%SZ')
    time = int((utc_dt - datetime(1970, 1, 1)).total_seconds())

    if eventName == "FeedAM" and utc_dt.hour >= 12:
        eventName = "FeedPM"


    post_message = {'name': actorName, "time": str(time), "event": eventName}

    response = snsClient.publish(
    TopicArn = catEventSNS,
    Message = json.dumps({"name": actorName, "time": time, "event": eventName}))
    print("Response: " + json.dumps(response, indent=2))

    speech_output = "Thank You! That record has been added!"

    return build_response({}, build_speechlet_response(
        card_title, speech_output, "", should_end_session))

def getPerformedChore(intent, session, event):
    card_title = intent['name']

    latestChores = lambdaClient.invoke(
        FunctionName = catGetPerformedLambda,
        InvocationType = 'RequestResponse'
        )
    payload = latestChores['Payload'].read()

    choresList = json.loads(json.loads(json.loads(payload)['body'])['Message'])

    eventName = ""
    if "value" in event["request"]["intent"]["slots"]["Cat"]:
        catName = event["request"]["intent"]["slots"]["Cat"]["value"]
        eventName = getActivity(event["request"]["intent"]["slots"]["Chore"]["value"], catName)
    else:
        eventName = getActivity(event["request"]["intent"]["slots"]["Chore"]["value"], "")

    selecteditem = {}
    if eventName != "FeedAM" and eventName != "FeedPM":
        for task in choresList:
            taskItem = task['item']
            if taskItem['task'] == eventName:
                selecteditem = task
                break
    else:
        feedAMTask = {}
        feedPMTask = {}
        for task in choresList:
            taskItem = task['item']
            if taskItem['task'] == "FeedAM":
                feedAMTask = task
            elif taskItem['task'] == "FeedPM":
                feedPMTask = task
            if feedAMTask and feedPMTask:
                break

        if int(feedAMTask['item']['time']) < int(feedPMTask['item']['time']):
            selecteditem = feedPMTask
        else:
            selecteditem = feedAMTask

    if selecteditem:
        lastTimeStamp = selecteditem['item']['time']
        lastPerson = selecteditem['item']['personName']
        lastStatus = selecteditem['status']
        lastChore = selecteditem['item']['task']

        lastDateTime = datetime.fromtimestamp(int(lastTimeStamp)) + TIMEZONE_DIFFERENCE
        lastTime = lastDateTime.strftime("%I:%M%p")
        lastDay = '{0:%A}, {0:%B} {0:%d}'.format(lastDateTime)
        speech_output = ""

        if lastChore == "FeedAM" or lastChore == "FeedPM":
            speech_output = speech_output + "The cat was last fed by "
        elif lastChore == "DownstairLitter":
            speech_output = speech_output + "The downstairs litter was last emptied by "
        elif lastChore == "UpstairLitter":
            speech_output = speech_output + "The upstairs litter was last emptied by "
        elif lastChore == "Vacuum":
            speech_output = speech_output + "The carpet was last vacuumed by "
        elif lastChore == "MillieNails":
            speech_output = speech_output + "Millie's nails were last clipped by "
        elif lastChore == "KittyXNails":
            speech_output = speech_output + "Kitty X's nails were last clipped by "


        speech_output = speech_output + str(lastPerson) + " at "+ str(lastTime) + " on " + str(lastDay) + ". "

        if lastStatus == "green":
            speech_output = speech_output + "The chore has been done recently, and does not need to be done at this time."
        elif lastStatus == "yellow":
            speech_output = speech_output + "The chore should be done soon, however can go a little bit longer before needing to be done."
        else:
            speech_output = speech_output + "The chore needs to be done. Please do the chore as soon as possible."

        print("Speech Output: " + speech_output)
        return build_response({}, build_speechlet_response(
            card_title, speech_output, "", True))
    else:
        speech_output = "Please make your request again, I did not understand your query. "
        return build_response({}, build_speechlet_response(
            card_title, speech_output, "Please ask me when a chore was done last or tell me that a chore has been completed. ", False))


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


def on_intent(intent_request, session, event):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "PerformChore":
        return performChore(intent, session, event)
    elif intent_name == "GetChore":
        return getPerformedChore(intent, session, event)
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
    Uncomment this if statement and populate with your sksill's application ID to
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
        return on_intent(event['request'], event['session'], event)
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
