from rest_framework.views import APIView
from django.http import HttpResponseRedirect
from rest_framework.response import Response
# from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import APIException, AuthenticationFailed

from .authentication import create_access_token, create_refresh_token, decode_access_token, decode_refresh_token
from .serializer import UserSerializer
from .models import User


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginAPIView(APIView):
    def post(self, request):
        user = User.objects.filter(email = request.data['email']).first()

        if not user:
            raise APIException('Invalid Credentials')
        
        if not user.check_password(request.data['password']):
            raise APIException('Invalid Credentials')
        
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        response = Response()

        response.set_cookie(key = 'refreshToken', value = refresh_token, httponly = True)
        response.data = {
            'token' : access_token
        }

        return response
    
class LogoutAPIView(APIView):
    def post(self, _):
        response = Response()
        response.delete_cookie(key = "refreshToken")
        response.data = {
            'message': "SUCCESS"
        }
        return response
    
class RefreshAPIView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refreshToken')
        id = decode_refresh_token(refresh_token)
        access_token = create_access_token(id)
        return Response({
            'token' : access_token
        })