from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Message

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'status']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    recipient = UserSerializer()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'content', 'timestamp', 'read']