# Generated by Django 3.0.6 on 2020-06-21 08:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0006_messages_documents'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messages',
            name='chat_id',
        ),
        migrations.AddField(
            model_name='messages',
            name='private_chat',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='chat.Chat'),
        ),
        migrations.AddField(
            model_name='messages',
            name='room_chat',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='chat.RoomChat'),
        ),
        migrations.AddField(
            model_name='roomchat',
            name='admin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
