from django.shortcuts import render
from rest_framework import permissions
from rest_framework.generics import *
from django.contrib.auth import get_user_model

from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.authtoken.models import Token

from .serializers import *
from .models import *

# @api_view(["POST"])
# def login(request):
#     username = request.data.get("username")
#     password = request.data.get("password")

#     user = authenticate(username=username, password=password)
#     if not user:
#         return Response({"error": "Login failed"}, status=HTTP_401_UNAUTHORIZED)

#     token, _ = Token.objects.get_or_create(user=user)
#     return Response({"token": token.key})

class RegistrationView(CreateAPIView):
	serializer_class = UserSerializer
	permission_classes = (permissions.AllowAny,)
	class Meta:
		model = User
		