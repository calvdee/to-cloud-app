"""
Use APIView for action-based views and leave other generics
for CRUD operations.

"""

from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from models import UrlUpload
from django_api_tocloud.serializers import (
	UrlUploadSerializer,
	UserSerializer) 
# from rest_framework import authentication, permissions

class UrlUploadListView(generics.ListCreateAPIView):
	"""
	List view for UrlUpload objects.
	"""
	model = UrlUpload
	serializer = UrlUploadSerializer


class UrlUploadRetrieveView(generics.RetrieveUpdateDestroyAPIView):
	"""
	Read/Update UrlUpload objects.
	"""
	model = UrlUpload
	serializer = UrlUploadSerializer


class UserListView(generics.ListCreateAPIView):
	"""
	List view for User objects.
	"""
	model = User
	serializer = UserSerializer


class UserRetrieveView(generics.RetrieveUpdateDestroyAPIView):
	"""
	Read/Write User objects.
	"""
	model = User
	serializer = UserSerializer