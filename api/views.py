from rest_framework.views import APIView
from rest_framework import status
from django.http import HttpResponseRedirect
from rest_framework.response import Response
# from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import APIException, AuthenticationFailed
from .authentication import create_access_token, create_refresh_token, decode_access_token, decode_refresh_token
from .serializer import UserSerializer, GeneratedTextSerializer, ResumeSerializer
from .models import User, Resume
import os
import openai

# Set your API key (either in your code or as an environment variable)

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
    
class ResumeBuilderView(APIView):
    def get(self, request, pk, format =None):
        # os.environ["OPENAI_API_KEY"] = "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"

        # openai.api_key = os.environ["OPENAI_API_KEY"]
        
        openai.api_key="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"
        if pk:
            resume_obj = Resume.objects.filter(id=pk).first()
            title = resume_obj.Name
            experience = resume_obj.experience
            skills = resume_obj.skills
            print(resume_obj.phone)
            prompt = f"Title: {title}\n\nabout: {experience}\n\nskills: {skills}\n\nPlease generate a resume summary for this candidate by mentioning all above data, starting the sentance with name"
            # Use the API to generate text
            response = openai.Completion.create(
                engine='text-davinci-003',
                prompt=prompt,
                max_tokens=50
            )
            print(response)
            generated_text = response.choices[0].text
            serializer = GeneratedTextSerializer({'generated_text': generated_text})
            # Print the generated text
            return Response(serializer.data, status=status.HTTP_200_OK)
    
        return HttpResponseRedirect("/")
        
class createResumeDataView(APIView):
    def post(self, request, format=None):
        data = request.data
        serializer = ResumeSerializer(data = data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)