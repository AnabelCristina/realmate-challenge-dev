# Generated by Django 5.1.6 on 2025-05-09 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_rename_conversation_message_conversation_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='closed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
