from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Q
from .serializers import UserSerializer, MessageSerializer
from .models import Message, Profile

class RegisterView(APIView):
    def post(self, request):
        try:
            data = request.data
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            if not username or not email or not password:
                return Response(
                    {'error': 'All fields (username, email, password) are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if User.objects.filter(username=username).exists():
                return Response(
                    {'error': 'Username already exists'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if User.objects.filter(email=email).exists():
                return Response(
                    {'error': 'Email already exists'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            Profile.objects.create(user=user)  # Create default profile
            return Response(
                {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'profile': {'profile_picture': '', 'status': user.profile.status}
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'error': f'Server error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class ProfileView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(UserSerializer(request.user).data)

    def put(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        profile = request.user.profile
        data = request.data
        profile.profile_picture = data.get('profile_picture', profile.profile_picture)
        profile.status = data.get('status', profile.status)
        profile.save()
        return Response(UserSerializer(request.user).data)

class ContactsView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        users = User.objects.exclude(id=request.user.id)
        return Response(UserSerializer(users, many=True).data)

class SearchUsersView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        query = request.query_params.get('q', '')
        if not query:
            return Response({'error': 'Search query is required'}, status=status.HTTP_400_BAD_REQUEST)
        users = User.objects.filter(
            Q(username__icontains=query) | Q(email__icontains=query)
        ).exclude(id=request.user.id)
        return Response(UserSerializer(users, many=True).data)

class MessageView(APIView):
    def get(self, request, recipient_id):
        if not request.user.is_authenticated:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            recipient = User.objects.get(id=recipient_id)
            messages = Message.objects.filter(
                Q(sender=request.user, recipient=recipient) |
                Q(sender=recipient, recipient=request.user)
            ).order_by('timestamp').select_related('sender', 'recipient')
            return Response(MessageSerializer(messages, many=True).data)
        except User.DoesNotExist:
            return Response({'error': 'Recipient not found'}, status=status.HTTP_404_NOT_FOUND)