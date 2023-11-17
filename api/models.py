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
    Name = models.CharField(max_length=255 , unique=True)
    email = models.CharField(max_length=255 , unique=True)
    phone = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255, null=False)
    education = models.CharField(max_length=255, null=False, default=None)
    experience = models.CharField(max_length=255, null=False, default=None)
    skills = models.CharField(max_length=255, null=True, default=None)
    github = models.CharField(max_length=255 , blank=True, null=True)
    behance = models.CharField(max_length=255 , blank=True, null=True)
    hackerank = models.CharField(max_length=255 , unique=True, null=True)
    summary = models.CharField(max_length=255 , unique=True, null=True)



class Project(models.Model):
    title = models.CharField(max_length=100, blank=False)
    stack = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.Title
    
class Company(models.Model):
    company_name = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ProjectLikes(models.Model):
    Company_id = models.ForeignKey(Company, on_delete = models.CASCADE, null = True, blank=False)
    Project_id = models.ForeignKey(Project, on_delete = models.CASCADE, null = True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
