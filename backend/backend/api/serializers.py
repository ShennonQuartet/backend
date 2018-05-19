from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Incident
from rest_framework.renderers import JSONRenderer
import json


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username')


class WriteUserSerializer(serializers.Serializer):
    pk = serializers.IntegerField(required=True)


class UserRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        serializer = UserSerializer(value)
        return serializer.data

    def to_internal_value(self, data):
        serializer = WriteUserSerializer(data=data)
        if serializer.is_valid():
            user = get_object_or_404(User, **serializer.validated_data)
            return user


class IncidentSerializer(serializers.ModelSerializer):
    user = UserRelatedField(queryset=User.objects, required=True)

    class Meta:
        model = Incident
        fields = ('pk', 'type', 'description', 'datetime', 'confirmed', 'user')