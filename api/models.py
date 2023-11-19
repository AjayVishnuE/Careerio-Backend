from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=255 , unique=True)
    email = models.CharField(max_length=255, unique=True)
    password =models.CharField(max_length=255)

    first_name = None
    last_name = None
    name = None

class Resume(models.Model):
    Name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    location = models.CharField(max_length=255, null=False)
    education = models.CharField(max_length=255, default="B.Tech")
    experience = models.CharField(max_length=255, default="0")
    skills = models.CharField(max_length=255, default="None")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resume')

class Projects(models.Model):
    title = models.CharField(max_length=255)
    companyname = models.CharField(max_length=255, default=None, null=True)
    description = models.TextField(default=None)
    deliverables = models.TextField(default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    stack = models.TextField(default=None)
    contributers = models.TextField(default=None)

class Gigs(models.Model):
    role = models.CharField(max_length=255)
    companyname = models.CharField(max_length=255,default=None, null=True)
    description = models.TextField(default=None)
    keyresponsibilities = models.TextField(default=None)
    qualifications = models.TextField(default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gigs')
    duration = models.CharField(max_length=255,default=None)
    amount = models.CharField(max_length=200, default=None)
    skills = models.TextField(default=None)

