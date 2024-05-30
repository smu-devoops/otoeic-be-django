from rest_framework import exceptions
from rest_framework import serializers

from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserDAO
        fields = [
            'id',
            'username',
            'level',
            'point',
            'freeze_amount',
            'freeze_activated',
            'streak',
            'date_created',
            'is_staff',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'username': {'read_only': True},
            'point': {'read_only': True},
            'freeze_amount': {'read_only': True},
            'streak': {'read_only': True},
            'date_created': {'read_only': True},
            'is_staff': {'read_only': True},
        }


class UsernamePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserDAO
        fields = [
            'id',
            'username',
            'password',
            'is_staff',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True},
            'is_staff': {'read_only': True},
        }

    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')

        if models.UserDAO.objects.filter(username=username).exists():
            exceptions.ValidationError(detail=(
                f"User with username {username} already exists."
            ))

        user: models.UserDAO = super().create(validated_data)
        user.set_password(password)
        return user


class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserDAO
        fields = [
            'id',
            'username',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'username': {'read_only': True},
        }
