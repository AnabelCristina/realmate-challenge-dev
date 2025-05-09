import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import models
from . import serializers

@api_view(['GET'])
def conversation_details(request, pk):
    conversation = models.Conversation.objects.get(id=pk)
    serializer = serializers.ConversationSerializer(conversation)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
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
    serializers.ConversationSerializer.create(data=data)

    print(f"Conversation {data.conversation_id} created.")

def handle_close_conversation(data):
    conversation = models.Conversation.objects.get(pk=data.get('data').get('id'))
    serializers.ConversationSerializer.update(conversation, data=data)
    
    print(f"Conversation {data.conversation_id} closed.")

def handle_new_message(data):
    conversation = models.Conversation.objects.get(pk=data.get('data').get('id'))
    if conversation.is_closed():
        return HttpResponseBadRequest("Conversation is closed, unable to send new messages.")

    serializers.MessageSerializer.create(data=data)
    
    print(f"Message received. message_id = {data.message_id}")
