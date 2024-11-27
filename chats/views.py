from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import MessageSerializer
from .models import Message
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        sender = request.user
        receiver_id = request.data.get('receiver')
        content = request.data.get('content')

        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            return Response({"message": "Receiver not found"}, status=404)

        message = Message.objects.create(
            sender=sender, receiver=receiver, content=content)
        serializer = MessageSerializer(message)

        return Response(serializer.data, status=201)


class GetMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        # Get the chat history between the current user and the given user_id
        user = request.user
        try:
            other_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=404)

        messages = Message.objects.filter(
            (Q(sender=user) & Q(receiver=other_user)) |
            (Q(sender=other_user) & Q(receiver=user))
        ).order_by('timestamp')

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


def chat_view(request):
    return render(request, 'chat.html')
