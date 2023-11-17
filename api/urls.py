from django.contrib import admin
from django.urls import path, include
from .views import RegisterAPIView, LoginAPIView, RefreshAPIView,LogoutAPIView,ResumeBuilderView,createResumeDataView

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('createresumedata/', createResumeDataView.as_view()),
    path('builder/<str:pk>/', ResumeBuilderView.as_view()),
]