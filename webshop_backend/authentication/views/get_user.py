from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        # Check if the user tokens are null
        if user.refresh_token is None or user.access_token is None:
            return Response({'error': 'User is logged out'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.refresh_token or not user.access_token:
            return Response({'error': 'User is logged out'}, status=status.HTTP_401_UNAUTHORIZED)

        user_data = {
            'username': user.username,
            'email': user.email,
        }
        return Response(user_data, status=status.HTTP_200_OK)
