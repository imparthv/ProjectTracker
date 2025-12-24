from rest_framework import serializers
from accounts.models import Account
from projects.models import Project
from tasks.models import Task

# Creating serializer for Account model
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'id','username', 'first_name', 'last_name', 'email',
        ]
        read_only_fields = ['email']

# Creating serializer to register user
class AccountRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = [
            'email', 
            'username',
            'password',
            'first_name',
            'last_name'
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Account(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
# Creating project serializer
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'status', 'owner', 'project_members','created_at', 'updated_at']
        read_only_fields = [
            'id', 'owner', 'created_at', 'updated_at', 
        ]

# Creating task serializer
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'status', 'priority',
                  'assigned_project','owner', 'assigned_to',
                  'created_at', 'updated_at']
        read_only_fields = [
            'id', 'owner', 'created_at', 'updated_at'
        ]