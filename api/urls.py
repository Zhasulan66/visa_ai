from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views


urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('chats/', views.ChatListCreateView.as_view(), name='chats'),
    path('chats/<int:chat_id>/messages/', views.MessageListCreateView.as_view(), name='chat-messages'),
]