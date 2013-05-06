from django.contrib.auth.models import User
from rest_framework import serializers
from django_api_tocloud.models import UrlUpload

class UrlUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlUpload


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User