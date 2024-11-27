from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import CustomUserSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.shortcuts import render

User = get_user_model()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully", "user": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                # Get the user by email
                user = User.objects.get(email=email)

                # Check if the password is correct
                if user.check_password(password):
                    # Create JWT tokens
                    refresh = RefreshToken.for_user(user)
                    access_token = refresh.access_token

                    # Return the response with user details and JWT token
                    return Response(
                        {
                            "message": "Login successful",
                            "user": {
                                "email": user.email,
                                "name": user.name,
                                "mobile": user.mobile,
                                "dob": user.dob,
                                "profile_picture": user.profile_picture.url if user.profile_picture else None
                            },
                            "access_token": str(access_token),
                            # Optionally include refresh token
                            "refresh_token": str(refresh)
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {"message": "Invalid credentials"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except User.DoesNotExist:
                return Response(
                    {"message": "Invalid credentials"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllUsers(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        instance = User.objects.all()
        serializer = CustomUserSerializer(instance, many=True)
        return Response({"Users": serializer.data}, status=status.HTTP_200_OK)


def register_view(request):
    return render(request, 'registration.html')


def login_view(request):
    return render(request, 'login.html')
