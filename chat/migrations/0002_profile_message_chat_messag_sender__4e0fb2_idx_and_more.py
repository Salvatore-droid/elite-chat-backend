# Generated by Django 5.2.4 on 2025-07-17 11:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.URLField(blank=True, null=True)),
                ('status', models.CharField(blank=True, default="Hey there! I'm using EliteChat", max_length=150)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['sender', 'recipient', 'timestamp'], name='chat_messag_sender__4e0fb2_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['recipient', 'sender', 'timestamp'], name='chat_messag_recipie_c405d1_idx'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
