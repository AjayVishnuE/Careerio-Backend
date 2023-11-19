from rest_framework.views import APIView
from rest_framework import status
from django.http import HttpResponseRedirect
from rest_framework.response import Response
# from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import APIException, AuthenticationFailed
from .authentication import create_access_token, create_refresh_token, decode_access_token, decode_refresh_token
from .serializer import UserSerializer, GeneratedTextSerializer, ResumeSerializer, ProjectSerializer, GigsSerializer, SkillSerializer
from .models import User, Resume, Projects, Gigs, Dashboard
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
        print(user)
        id = user.id
        name=user.username
        email = user.email

        if not user:
            raise APIException('Invalid Credentials')
        
        if not user.check_password(request.data['password']):
            raise APIException('Invalid Credentials')
        
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        response = Response()

        response.set_cookie(key = 'refreshToken', value = refresh_token, httponly = True)
        response.data = {
            'token' : access_token,
            'id' : id,
            'username':name,
            'email':email
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
    def get(self, request, format =None):
        data = request.data
        serializer1 = ResumeSerializer(data = data)
        # os.environ["OPENAI_API_KEY"] = "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"

        # openai.api_key = os.environ["OPENAI_API_KEY"]
        
        openai.api_key="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"
        if data:
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
            serializer2 = GeneratedTextSerializer({'generated_text': generated_text})
            # Print the generated text

            return Response(serializer.data, status=status.HTTP_200_OK)
    
        return HttpResponseRedirect("/")
        
class createResumeDataView(APIView):
    def post(self, request, format=None):
        data = request.data
        token = request.headers.get('Authorization', '').split(' ')[1]
        user_id = decode_access_token(token)
        print(user_id)
        print("Request Data:", request.data)
        data['user']=user_id
        serializer = ResumeSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            print("Serializer Data:", serializer.data)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request,format=None):
        data = request.data
        token = request.headers.get('Authorization', '').split(' ')[1]
        user_id = decode_access_token(token)
        try:
            obj = Resume.objects.get(id=user_id)
        except Resume.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ResumeSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class createProjectsView(APIView):
    def post(self, request, format=None):
        data = request.data
        token = request.headers.get('Authorization', '').split(' ')[1]
        user_id = decode_access_token(token)
        print(user_id)
        print("Request Data:", request.data)
        data['user']=user_id
        serializer = ProjectSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            print("Serializer Data:", serializer.data)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
class createGigsView(APIView):
    def post(self, request, format=None):
        data = request.data
        token = request.headers.get('Authorization', '').split(' ')[1]
        user_id = decode_access_token(token)
        print(user_id)
        print("Request Data:", request.data)
        data['user']=user_id
        serializer = GigsSerializer(data = data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            print("Serializer Data:", serializer.data)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class ProjectsUserDisplayView(APIView):
    def get(self, request, format =None):
        token = request.headers.get('Authorization', '').split(' ')[1]
        user_id = decode_access_token(token)
        print(user_id)
        if user_id:
            print("test")
            queryset = Projects.objects.all().filter(user=user_id)
            serializer = ProjectSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
class GigsUserDisplayView(APIView):
    def get(self, request, format =None):
        token = request.headers.get('Authorization', '').split(' ')[1]
        user_id = decode_access_token(token)
        print(user_id)
        if user_id:
            print("test")
            queryset = Gigs.objects.all().filter(user=user_id)
            serializer = GigsSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class AllProjectDisplayView(APIView):
    def get(self,request, format=None):
            queryset = Projects.objects.all()
            serializer = ProjectSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

class AllGigDisplayView(APIView):
    def get(self,request, format=None):
            queryset = Gigs.objects.all()
            serializer = GigsSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

class AllResumeDisplayView(APIView):
    def get(self,request, format=None):
            queryset = Resume.objects.all()
            serializer = ResumeSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

class SkillSearchView(APIView):
    def get(self, request, format=None):
        query = request.data
        print(query)
        queryset = Resume.objects.filter(skills__icontains=query) 
        serializer = ResumeSerializer(queryset, many=True)
        return Response(serializer.data)

    # def get(self, request, format=None):
    #     query = request.data
    #     print(query)
    #     queryset = Resume.objects.filter(skills__icontains=query).prefetch_related('resume')
    #     serializer = ResumeSerializer(queryset, many=True)
    #     return Response(serializer.data)


class DashboardDetailsView(APIView):
    def get(self,request,format=None):
        totalprojects = Projects.objects.count()
        totalgigs = Gigs.objects.count()
        print(totalprojects,totalgigs)
        token = request.headers.get('Authorization', '').split(' ')[1]
        user_id = decode_access_token(token)
        print(user_id)
        if user_id:
            visit_obj = Dashboard.objects.get(user=user_id)
            serializer = DashboardSerializer(visit_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def patch(self, request,pk, format=None):
        obj = Dashboard.objects.get(pk=pk)
        serializer = DashboardSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


