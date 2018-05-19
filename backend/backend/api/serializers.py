from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Incident


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
            user = User.objects.filter(**serializer.validated_data).first()
            if not user:
                raise serializers.ValidationError("User should exist")
            return user
        else:
            raise(serializer.errors)


class IncidentSerializer(serializers.ModelSerializer):
    user = UserRelatedField(queryset=User.objects, required=True)

    class Meta:
        model = Incident
        fields = ('pk', 'type', 'description', 'datetime', 'confirmed', 'user')