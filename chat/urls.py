from django.urls import path
from .views import RegisterView, LoginView, ContactsView, MessageView, ProfileView, SearchUsersView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('search/', SearchUsersView.as_view(), name='search_users'),
    path('messages/<int:recipient_id>/', MessageView.as_view(), name='messages'),
]