from. import models

def conversation_exists(data):
    conversation = models.Conversation.objects.filter(pk=data.get('data').get('id'))
    return conversation.exists()

def message_exists(data):
    message = models.Message.objects.filter(pk=data.get('data').get('id'))
    return message.exists()

def conversation_is_closed(data):
    conversation = models.Conversation.objects.get(pk=data.get('data').get('conversation_id'))
    return conversation.is_closed()

def message_direction(data):
    return data.get('data').get('direction')
    