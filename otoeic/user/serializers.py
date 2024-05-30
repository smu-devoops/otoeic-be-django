from rest_framework import exceptions
from rest_framework import serializers

from . import models


class UsernamePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserDAO
        fields = [
            'id',
            'username',
            'password',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True},
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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserDAO
        fields = [
            'id',
            'username',
            'level',
            'streak_freeze_amount',
            'is_streak_freeze_activated',
            'point',
            'is_staff',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'is_staff': {'read_only': True},
        }
