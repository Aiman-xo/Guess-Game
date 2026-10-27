from rest_framework import serializers
from authapp.models import MainUser
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True,validators=[validate_password])

    def validate_email(self,value):
        if MainUser.objects.filter(email = value).exists():
            raise serializers.ValidationError('there has been an email exists already!')
        return value

    def validate_username(self,value):
        if MainUser.objects.filter(username=value):
            raise serializers.ValidationError('username already exists!')
        return value

    def create(self,validated_data):
        user = MainUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=validated_data['username']
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()