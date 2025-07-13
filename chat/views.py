from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .serializers import UserSerializer, MessageSerializer
from .models import Message

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        if User.objects.is_none() or User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, email=email, password=password)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class ContactsView(APIView):
    def get(self, request):
        users = User.objects.exclude(id=request.user.id)
        return Response(UserSerializer(users, many=True).data)

class MessageView(APIView):
    def get(self, request, recipient_id):
        messages = Message.objects.filter(
            models.Q(sender=request.user, recipient_id=recipient_id) |
            models.Q(sender_id=recipient_id, recipient=request.user)
        ).order_by('timestamp')
        return Response(MessageSerializer(messages, many=True).data)