from django.contrib import admin
from django.urls import path, include
from .views import RegisterAPIView, LoginAPIView, RefreshAPIView,LogoutAPIView,ResumeBuilderView,createResumeDataView,ProjectsUserDisplayView, createProjectsView, GigsUserDisplayView, createGigsView, DashboardDetailsView, AllProjectDisplayView, AllGigDisplayView, AllResumeDisplayView, SkillSearchView

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('createresumedata/', createResumeDataView.as_view()),
    path('builder/<str:pk>/', ResumeBuilderView.as_view()),
    path('createproject/', createProjectsView.as_view()),
    path('projectuserlist/', ProjectsUserDisplayView.as_view()),
    path('creategig/', createGigsView.as_view()),
    path('giguserlist/', GigsUserDisplayView.as_view()),
    path('dashboard/', DashboardDetailsView.as_view()),
    path('allprojects/', AllProjectDisplayView.as_view()),
    path('allgigs/', AllGigDisplayView.as_view()),
    path('allresume/', AllResumeDisplayView.as_view()),
    path('search/', SkillSearchView.as_view()),
    

    
]