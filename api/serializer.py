from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import User, Resume, Projects, Gigs

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = (
        'id', 
        'Name', 
        'email',
        'phone',
        'location',
        'education', 
        'experience',   
        'skills',
        'user'
        )

    def create(self, validated_data):
        return Resume.objects.create(**validated_data )
        


class GeneratedTextSerializer(serializers.Serializer):
    generated_text = serializers.CharField()


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = (
            'id', 
            'title', 
            'companyname',
            'description',
            'deliverables',
            'stack', 
            'user',
            'contributers',   
        )


    def create(self, validated_data):
        return Projects.objects.create(**validated_data )
    
    
class GigsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gigs
        fields = (
        'id', 
        'role', 
        'companyname',
        'description',
        'keyresponsibilities',
        'qualifications', 
        'user',
        'duration',   
        'amount',
        'skills'
        )

    def create(self, validated_data):
        return Gigs.objects.create(**validated_data )