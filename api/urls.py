from django.contrib import admin
from django.urls import path, include
from .views import RegisterAPIView, LoginAPIView, RefreshAPIView,LogoutAPIView,ResumeBuilderView,createResumeDataView,ProjectsDisplayView, createProjectsView, GigsDisplayView, createGigsView

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('createresumedata/', createResumeDataView.as_view()),
    path('builder/<str:pk>/', ResumeBuilderView.as_view()),
    path('createproject/', createProjectsView.as_view()),
    path('project/<str:pk>/', ProjectsDisplayView.as_view()),
    path('creategig/', createGigsView.as_view()),
    path('gig/<str:pk>/', GigsDisplayView.as_view()),
]