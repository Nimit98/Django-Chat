# Generated by Django 3.0.6 on 2020-07-05 17:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0020_auto_20200705_2030'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='notificationprivate',
            name='count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='notificationprivate',
            name='sender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification', to='chat.UserList'),
        ),
    ]
