from django.db import models
import uuid

class Conversation(models.Model):

    class StateChoices(models.TextChoices):
        OPEN = "OPEN"
        CLOSED = "CLOSED"
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    state = models.CharField(max_length=10, choices=StateChoices.choices, default=StateChoices.OPEN)
    created_at = models.DateTimeField()
    closed_at = models.DateTimeField()

    @property
    def is_open(self):
        return self.state == "OPEN"
    
    def create_conversation(self, id, state, created_at):
        conversation = self.create(id = id, state = state, created_at = created_at)
        return conversation

class Message(models.Model):
    class TypeChoices(models.TextChoices):
        SENT = "SENT"
        RECEIVED = "RECEIVED"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    message_type = models.CharField(max_length=10, choices=TypeChoices.choices, default=TypeChoices.SENT)
    content = models.TextField()
    created_at = models.DateTimeField()
    conversation_id = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    def new_message(self, id, message_type, created_at, content, conversation_id):
        conversation = self.create(id = id, message_type = message_type, created_at = created_at, content = content, conversation_id = conversation_id)
        return conversation

