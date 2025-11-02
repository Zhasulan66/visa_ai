from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .models import Chat, Message, Subscription, EsimOrder, Consultant
from .serializers import RegisterSerializer, ChatSerializer, MessageSerializer, SubscriptionSerializer, \
    EsimOrderSerializer, ConsultantSerializer

User = get_user_model()

# Registration
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


# Chat list + create
class ChatListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatSerializer

    def get_queryset(self):
        return Chat.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Messages (list + create)
class MessageListCreateView(APIView):
    def get(self, request, chat_id):
        chat = Chat.objects.filter(id=chat_id, user=request.user).first()
        if not chat:
            return Response({'error': 'Chat not found or no access'}, status=404)
        messages = chat.messages.all().order_by('created_at')
        return Response(MessageSerializer(messages, many=True).data)

    def post(self, request, chat_id):
        chat = Chat.objects.filter(id=chat_id, user=request.user).first()
        if not chat:
            return Response({'error': 'Chat not found or no access'}, status=404)

        content = request.data.get('content')
        message = Message.objects.create(
            chat=chat,
            sender=request.user,
            content=content
        )
        return Response(MessageSerializer(message).data)

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.AllowAny]  # later can be IsAuthenticated


class EsimOrderViewSet(viewsets.ModelViewSet):
    queryset = EsimOrder.objects.all()
    serializer_class = EsimOrderSerializer
    permission_classes = [permissions.AllowAny]


class ConsultantViewSet(viewsets.ModelViewSet):
    queryset = Consultant.objects.all()
    serializer_class = ConsultantSerializer
    permission_classes = [permissions.AllowAny]
