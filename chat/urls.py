from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('search/', views.SearchUsersView.as_view(), name='search'),
    path('messages/<int:recipient_id>/', views.MessageView.as_view(), name='messages'),
]