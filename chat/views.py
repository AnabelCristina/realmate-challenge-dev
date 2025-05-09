import json
from django.forms import ValidationError
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status]
from .handlers import handle_close_conversation, handle_new_conversation, handle_new_message
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

    try:
        if event_type == "NEW_CONVERSATION":
            return handle_new_conversation(data)
        elif event_type == "CLOSE_CONVERSATION":
            return handle_close_conversation(data)
        elif event_type == "NEW_MESSAGE":
            return handle_new_message(data)
        else:
            return HttpResponseBadRequest("Unhandled event type.")
    except ValidationError:
        return HttpResponseBadRequest("Id is not valid.")


