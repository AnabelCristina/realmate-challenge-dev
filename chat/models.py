from django.db import models
import uuid

class Conversation(models.Model):

    class StateChoices(models.TextChoices):
        OPEN = "OPEN"
        CLOSED = "CLOSED"
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    state = models.CharField(max_length=10, choices=StateChoices.choices, default=StateChoices.OPEN)
    created_at = models.DateTimeField()

    def is_open(self):
        return self.state == "OPEN"

class Message(models.Model):
    class TypeChoices(models.TextChoices):
        SENT = "SENT"
        RECEIVED = "RECEIVED"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    state = models.CharField(max_length=10, choices=TypeChoices.choices, default=TypeChoices.SENT)
    content = models.TextField()
    created_at = models.DateTimeField()
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )

