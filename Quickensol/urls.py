from django.contrib import admin
from django.urls import path, include
from userauth.views import register_view, login_view
from chats.views import chat_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('userauth.urls')),
    path('api/', include('chats.urls')),
    path('register/', register_view, name='register'),  # Render the template
    path('login/', login_view, name='login'),
    path('chat/', chat_view, name='chat'),
]
