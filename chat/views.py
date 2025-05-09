import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from chat import models

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
        handle_new_message(data)
    else:
        return HttpResponseBadRequest("Unhandled event type.")

    return JsonResponse({"status": "success"})

def handle_new_conversation(data):
    timestamp = data["timestamp"]
    conversation_id = data["data"]["id"]
    
    new_conversation = models.Conversation.create_conversation(conversation_id, "OPEN", timestamp)
    new_conversation.save()
    
    print(f"Conversation {conversation_id} created.")

def handle_close_conversation(data):
    timestamp = data["timestamp"]
    conversation_id = data["data"]["id"]
   
    conversation = models.Conversation.objects.get(pk=conversation_id)
    conversation.state = "CLOSED"
    conversation.closed_at = timestamp
    conversation.save()
    
    print(f"Conversation {conversation_id} closed.")

def handle_new_message(data):

    conversation = models.Conversation.objects.get(pk=conversation_id)
    if conversation.is_closed():
        return HttpResponseBadRequest("Conversation is closed, unable to send new messages.")

    timestamp = data["timestamp"]
    conversation_id = data["data"]["conversation_id"]
    message_id = data["data"]["id"]
    message = data["data"]["content"]
    message_type = data["data"]["direction"]

    new_message = models.Message.new_message(message_id, message_type, timestamp, message, conversation_id)
    new_message.save()
    
    print(f"Message received. message_id = {message_id}")
