from rest_framework import serializers
from .models import Message, Conversation

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
    
    def create(data):
        id = data.get('data').get('id')
        message_type = data.get('data').get('direction')
        content = data.get('data').get('content')
        created_at = data.get('timestamp')
        conversation_id = data.get('data').get('conversation_id')

        return Message.objects.create(id=id, message_type = message_type, content=content, 
                                             created_at=created_at, conversation_id=conversation_id)
                                      
    

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    class Meta:
        model = Conversation
        fields = ['id', 'created_at', 'closed_at', 'state', 'messages']

    def create(data):
        id = data.get('data').get('id')
        state = "OPEN"
        created_at = data.get('timestamp')

        return Conversation.objects.create(id=id, state = state, created_at = created_at)

    def close(instance, data):
        instance.state = data.get('state', "CLOSED")
        instance.closed_at = data.get('closed_at', instance.closed_at)
        instance.save()
        return instance


    