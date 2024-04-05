from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


# from user.serializers import UserSerializer


# Class based view to Get User Details using Token Authentication
class UserDetailAPI(APIView):
    authentication_classes = (TokenAuthentication,)

    # permission_classes = (AllowAny,)
    def get(self, request, *args, **kwargs):
        user = User.objects.get(
            id=request.user.id
        )  # insance , single instance , multiple data ( error )
        # user = User.objects.filter(name=request.data["name"]) #queryset  , multiple
        serializer = UserSerializer(user)
        return Response(serializer.data)


# Class based view to register user
class RegisterUserAPIView(generics.CreateAPIView):
    #permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

#class based view to login
class LoginUserAPIView(APIView):
    
    # permission_classes = (AllowAny,)

    # permission_classes=[IsAuthenticate]
    
    def post(self, request, *args, **kwargs):
      username = request.data.get("username")
      password= request.data.get("password")

      print(username)
      print(password)

      user = authenticate(username=username, password=password)
      print(user)
      if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key},status=200)
      else:
            return Response({'error': 'Invalid credentials'}, status=401)

      


# view authenticate 

class AuthenticateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=200)
        # user= request.user.a
        # return Response(
        #     {"id":request.user.id,"firstname":request.user.username,"email":request.user.email}
        #     , status=200
        # )   
        
       
        

       



