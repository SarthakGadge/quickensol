from django.urls import path
from .views import RegisterView, LoginView, AllUsers

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/', AllUsers.as_view(), name='login')
]
