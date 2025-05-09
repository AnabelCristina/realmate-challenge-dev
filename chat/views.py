import json
from django.forms import ValidationError
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .services import get_conversation_by_id
from .handlers import handle_close_conversation, handle_new_conversation, handle_new_message
from . import models
from . import serializers

@api_view(['GET'])
def conversation_details(request, pk):
    conversation = get_conversation_by_id(pk)
    return Response(conversation.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@csrf_exempt 
def conversation_webhook(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request method.")

    try:
        data = json.loads(request.body)
        event_type = data.get("type")

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
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON payload.")


