import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt 
def conversation_webhook(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request method.")

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON payload.")

    # Perform different actions based on the event type
    event_type = data.get("type")

    if event_type == "NEW_CONVERSATION":
        handle_new_conversation(data)
    elif event_type == "CLOSE_CONVERSATION":
        handle_close_conversation(data)
    elif event_type == "NEW_MESSAGE":
        if data.get("data").get("direction") == "RECEIVED":
            handle_message_received(data)
        if data.get("data").get("direction") == "SENT":
            handle_message_sent(data)
    else:
        return HttpResponseBadRequest("Unhandled event type.")

    return JsonResponse({"status": "success"})

def handle_new_conversation(data):
    timestamp = data["timestamp"]
    conversation_id = data["data"]["id"]
    #Update the database // notify the user
    print(f"Conversartion {conversation_id} created.")

def handle_close_conversation(data):
    timestamp = data["timestamp"]
    conversation_id = data["data"]["id"]
    #Update the database // notify the user
    print(f"Conversartion {conversation_id} closed.")

def handle_message_received(data):
    timestamp = data["timestamp"]
    conversation_id = data["data"]["conversation_id"]
    message_id = data["data"]["id"]
    message = data["data"]["content"]
    #Update the database // notify the user
    print(f"Message received. message_id = {message_id}")

def handle_message_sent(data):
    timestamp = data["timestamp"]
    conversation_id = data["data"]["conversation_id"]
    message_id = data["data"]["id"]
    message = data["data"]["content"]
    #Update the database // notify the user
    print(f"Message sent. message_id = {message_id}")