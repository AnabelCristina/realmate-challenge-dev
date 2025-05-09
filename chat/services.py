from .models import Message, Conversation
from rest_framework.response import Response
from .serializers import ConversationSerializer
from rest_framework import status

def conversation_is_closed(id):
    conversation = Conversation.objects.get(pk=id)
    return conversation.is_closed()

def message_direction(data):
    return data.get('data').get('direction')
    
def create_conversation(data):
    id = data.get('data').get('id')
    state = "OPEN"
    created_at = data.get('timestamp')

    Conversation.objects.create(id=id, state = state, created_at = created_at)

def close_conversation(data, id):
    conversation = Conversation.objects.get(pk=id)
    conversation.state = "CLOSED"
    conversation.closed_at = data.get('timestamp')
    conversation.save()

def create_message(data):
    id = data.get('data').get('id')
    message_type = data.get('data').get('direction')
    content = data.get('data').get('content')
    created_at = data.get('timestamp')
    conversation_id = Conversation.objects.get(pk=data.get('data').get('conversation_id'))

    Message.objects.create(id=id, message_type = message_type, content=content, 
                                            created_at=created_at, conversation_id=conversation_id)
    
def get_conversation_by_id(id):
    conversation = Conversation.objects.get(pk=id)
    return ConversationSerializer(conversation)
