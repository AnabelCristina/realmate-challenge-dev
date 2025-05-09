from django.http import HttpResponseBadRequest
from rest_framework.response import Response
from rest_framework import status
from . import models
from . import serializers
from .services import conversation_exists, conversation_is_closed, message_exists, message_direction

def handle_new_conversation(data):
    if conversation_exists(data):
       return HttpResponseBadRequest("Invalid Conversation ID. ID already in use.")
    
    serializers.ConversationSerializer.create(data=data)
    return Response(status=status.HTTP_200_OK)

def handle_close_conversation(data):
    if not conversation_exists(data):
       return HttpResponseBadRequest("Invalid ID. ID doesn't exists.")
    
    if conversation_is_closed(data):
        return HttpResponseBadRequest("Conversation is closed already.")

    conversation = models.Conversation.objects.get(pk=data.get('data').get('conversation_id'))
    serializers.ConversationSerializer.close(conversation, data=data)
    return Response(status=status.HTTP_200_OK)

def handle_new_message(data):

    if not conversation_exists(data):
        return HttpResponseBadRequest("Conversation doesn't exists.")
    
    if conversation_is_closed(data):
        return HttpResponseBadRequest("Conversation is closed, unable to send new messages.")
    
    if message_exists(data):
        return HttpResponseBadRequest("Invalid Message ID. ID already in use.")
    
    if message_direction(data) not in ['RECEIVED', 'SENT']:
        return HttpResponseBadRequest("Invalid direction. Values allowed are 'RECEIVED' or 'SENT'.")

    serializers.MessageSerializer.create(data=data)
    return Response(status=status.HTTP_200_OK)