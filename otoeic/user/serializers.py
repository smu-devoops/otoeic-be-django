from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    streak = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id',
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
            'password': {'write_only': True},
            'profile_image': {'required': False, 'write_only': True},
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def get_streak(self, obj: User):
        # TODO
        return 0