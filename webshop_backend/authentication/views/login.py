from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import User
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username_or_email = request.data.get('username_or_email')
        password = request.data.get('password')
        print(username_or_email)
        print(password)
        user = authenticate(username=username_or_email, password=password) or \
               User.objects.filter(email=username_or_email).first()
        
        print(user)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            user.refresh_token = str(refresh)  # Save the refresh token
            user.access_token = str(refresh.access_token)  # Save the access token
            user.save()
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

