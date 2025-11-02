from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views
from .views import SubscriptionViewSet, EsimOrderViewSet, ConsultantViewSet

router = DefaultRouter()
router.register("consultants", ConsultantViewSet)
router.register("subscriptions", SubscriptionViewSet)
router.register("esim-orders", EsimOrderViewSet)

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('chats/', views.ChatListCreateView.as_view(), name='chats'),
    path('chats/<int:chat_id>/messages/', views.MessageListCreateView.as_view(), name='chat-messages'),

    path('', include(router.urls)),
]