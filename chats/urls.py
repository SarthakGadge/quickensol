from django.urls import path
from .views import SendMessageView, GetMessagesView

urlpatterns = [
    path('send-message/', SendMessageView.as_view(), name='send-message'),
    path('messages/<int:user_id>/', GetMessagesView.as_view(), name='get-messages'),

]
