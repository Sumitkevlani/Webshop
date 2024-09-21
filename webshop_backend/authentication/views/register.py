from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import User
from rest_framework.permissions import AllowAny
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.exceptions import ObjectDoesNotExist

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        email = request.data.get('email')

        # Validate username and password
        if len(username) < 8 or ' ' in username:
            return Response({'error': 'Username must be at least 8 characters and cannot contain spaces'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            pass  # Username does not exist, proceed with registration

        try:
            user = User.objects.get(email=email)
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            pass  # Email does not exist, proceed with registration


        if password != confirm_password:
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(password=password)
        except DjangoValidationError as e:
            return Response({'error': list(e.messages)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
