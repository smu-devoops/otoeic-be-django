from rest_framework import serializers

from user.models import UserDAO


class UserSerializer(serializers.ModelSerializer):
    is_admin = serializers.SerializerMethodField()
    streak = serializers.SerializerMethodField()

    class Meta:
        model = UserDAO
        fields = ['id',
                  'is_admin',
                  'password',
                  'username',
                  'level',
                  'streak',
                  'streak_freeze_amount',
                  'is_streak_freeze_activated',
                  'point']
        extra_kwargs = {
            'id': {'read_only': True},
            'email': {'write_only': True},
            'is_admin': {'read_only': True},
        }

    def get_is_admin(self, obj: UserDAO) -> bool:
        return obj.is_superuser

    def get_streak(self, obj: UserDAO):
        # TODO
        return 0
