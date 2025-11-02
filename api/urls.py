from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"consultants", views.ConsultantViewSet)
router.register(r"subscriptions", views.SubscriptionViewSet)
router.register(r"esim-orders", views.EsimOrderViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("chats/", views.ChatListCreateView.as_view(), name="chats"),
    path("chats/<int:chat_id>/messages/", views.MessageListCreateView.as_view(), name="chat-messages"),
]