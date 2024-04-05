# from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

#from palika.models import UserAuth
from palika.serializers import SignUpSerializers

# 2. Create
class SignUpApiView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[
                "username",
                "password",
                "email",
                "firstname",
                "lastname",
            ],
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING),
                "email": openapi.Schema(type=openapi.TYPE_STRING),
                "firstname": openapi.Schema(type=openapi.TYPE_STRING),
                "lastname": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    )
    def post(self, request, *args, **kwargs):
        
        data = {
            "username": request.data.get("username"),
            "password": request.data.get("password"),
            "email": request.data.get("email"),
            "firstname": request.data.get("firstname"),
            "lastname": request.data.get("lastname"),
        }
        serializer = SignUpSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
