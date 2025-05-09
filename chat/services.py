from .models import Message, Conversation

def conversation_exists(data):
    conversation = Conversation.objects.filter(pk=data.get('data').get('id'))
    return conversation.exists()

def message_exists(data):
    message = Message.objects.filter(pk=data.get('data').get('id'))
    return message.exists()

def conversation_is_closed(data):
    conversation = Conversation.objects.get(pk=data.get('data').get('conversation_id'))
    return conversation.is_closed()

def message_direction(data):
    return data.get('data').get('direction')
    
def create_conversation(data):
    id = data.get('data').get('id')
    state = "OPEN"
    created_at = data.get('timestamp')

    Conversation.objects.create(id=id, state = state, created_at = created_at)

def close_conversation(instance, data):
    instance.state = data.get('state', "CLOSED")
    instance.closed_at = data.get('closed_at', instance.closed_at)
    instance.save()

def create_message(data):
    id = data.get('data').get('id')
    message_type = data.get('data').get('direction')
    content = data.get('data').get('content')
    created_at = data.get('timestamp')
    conversation_id = Conversation.objects.get(pk=data.get('data').get('conversation_id'))

    Message.objects.create(id=id, message_type = message_type, content=content, 
                                            created_at=created_at, conversation_id=conversation_id)
