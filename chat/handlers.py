from django.db import IntegrityError
from django.http import HttpResponseBadRequest, JsonResponse
from rest_framework.response import Response
from rest_framework import status
from .models import Conversation
from .services import conversation_is_closed, message_direction, create_conversation, close_conversation, create_message

def handle_new_conversation(data):
    try:
        create_conversation(data=data)
        return Response(status=status.HTTP_200_OK)
    
    except IntegrityError:
        return JsonResponse({"status": "error", "message": "Invalid Conversation ID. ID already in use."}, status= 400)
    except Exception as e:
        return Response(e, status = 400)

def handle_close_conversation(data):
    try:
        conversation_id = data.get('data').get('id')

        if conversation_is_closed(conversation_id):
            return HttpResponseBadRequest("Conversation is already closed.")
        
        close_conversation(data, conversation_id)
        return Response(status=status.HTTP_200_OK)
    
    except Conversation.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Invalid Conversation ID. Conversation doesn't exists."}, status= 400)
    except Exception as e:
        return Response(e, status = 400)

def handle_new_message(data):
    try:
        if conversation_is_closed(data.get('data').get('conversation_id')):
            return HttpResponseBadRequest("Conversation is closed, unable to send new messages.")
        
        if message_direction(data) not in ['RECEIVED', 'SENT']:
            return HttpResponseBadRequest("Invalid direction. Values allowed are 'RECEIVED' or 'SENT'.")

        create_message(data=data)
        return Response(status=status.HTTP_200_OK)
    
    except Conversation.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Invalid Conversation ID. Conversation doesn't exists."}, status= 400)
    except IntegrityError:
        return JsonResponse({"status": "error", "message": "Invalid Message ID. ID already in use."}, status= 400)
    except Exception as e:
        return Response(e, status = 400)