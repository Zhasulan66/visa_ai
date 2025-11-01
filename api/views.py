from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .models import Chat, Message
from .serializers import RegisterSerializer, ChatSerializer, MessageSerializer

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


