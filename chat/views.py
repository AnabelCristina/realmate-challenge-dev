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
        return handle_new_conversation(data)
    elif event_type == "CLOSE_CONVERSATION":
        return handle_close_conversation(data)
    elif event_type == "NEW_MESSAGE":
        return handle_new_message(data)
    else:
        return HttpResponseBadRequest("Unhandled event type.")


def handle_new_conversation(data):
    conversation = models.Conversation.objects.filter(pk=data.get('data').get('id'))
    
    if conversation.exists():
       return HttpResponseBadRequest("Invalid ID. ID already in use.")
    
    serializers.ConversationSerializer.create(data=data)
    return JsonResponse({"status": "success"})

def handle_close_conversation(data):

    conversation = models.Conversation.objects.filter(pk=data.get('data').get('id'))

    if not conversation.exists():
       return HttpResponseBadRequest("Invalid ID. ID doesn't exists.")
    
    conversation = models.Conversation.objects.get(pk=data.get('data').get('id'))
    serializers.ConversationSerializer.close(conversation, data=data)
    
    return JsonResponse({"status": "success"})

def handle_new_message(data):
    conversation = models.Conversation.objects.get(pk=data.get('data').get('id'))
    if conversation.is_closed():
        return HttpResponseBadRequest("Conversation is closed, unable to send new messages.")

    serializers.MessageSerializer.create(data=data)
    
    return JsonResponse({"status": "success"})
