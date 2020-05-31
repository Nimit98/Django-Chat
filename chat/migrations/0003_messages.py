# Generated by Django 3.0.6 on 2020-05-28 06:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_chat'),
    ]

    operations = [
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('messages', models.CharField(max_length=200)),
                ('user', models.CharField(max_length=200)),
                ('chat_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.Chat')),
            ],
        ),
    ]
