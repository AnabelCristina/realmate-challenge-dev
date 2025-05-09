from django.contrib import admin
from chat import models

admin.site.register(models.Conversation)
admin.site.register(models.Message)
# Register your models here.
