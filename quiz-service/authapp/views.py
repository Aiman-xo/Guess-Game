from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import RegisterSerializer,LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import authenticate

# Create your views here.

class RegisterView(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'User creation successful!'},status=status.HTTP_201_CREATED)
        return Response({'error':'there has been a problem in user creation!','error_message':f'{serializer.error_messages}'},status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self,request):
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(request,email=email,password=password)
        if not user:
            return Response({'error':'couldnt login!'},status=status.HTTP_400_BAD_REQUEST)

        refresh_token = RefreshToken.for_user(user)

        response = Response({
            'access_token':str(refresh_token.access_token),
            'message':'login successful!'
        })

        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            secure=True,
            samesite='lax',
            httponly=True
        )
        return response

class CookieRefreshView(APIView):
    def post(self,request):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'error':'there is no refresh token!'},status=status.HTTP_400_BAD_REQUEST)

        try:
            new_refresh = RefreshToken(refresh_token)
        except TokenError:
            return Response({"error":'couldnt fetch essential credentials!'},status=status.HTTP_400_BAD_REQUEST)

        new_access = str(new_refresh.access_token)

        return Response({'message':'token geneation complete',"access_token":new_access})

class HealthCheck(APIView):
    def get(self,request):
        return Response({'status':'ok'})