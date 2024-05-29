from rest_framework import serializers

from .models import UserDAO


class UsernamePasswordSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDAO
        fields = [
            'id',
            'username',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'username': {'read_only': True},
        }


class UserSerializer(serializers.ModelSerializer):
    is_admin = serializers.SerializerMethodField()
    streak = serializers.SerializerMethodField()

    class Meta:
        model = UserDAO
        fields = [
            'id',
            'username',
            'is_admin',
            'level',
            'streak',
            'streak_freeze_amount',
            'is_streak_freeze_activated',
            'point'
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'email': {'write_only': True},
            'is_admin': {'read_only': True},
        }

    def get_is_admin(self, obj: UserDAO) -> bool:
        return obj.is_staff

    def get_streak(self, obj: UserDAO):
        # TODO
        return 0
