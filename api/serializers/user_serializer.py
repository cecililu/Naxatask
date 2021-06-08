from user.models import UserProfile
from rest_framework import serializers


class UserProfileSerializer(serializers.ModelSerializer):
    is_active = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = '__all__'

    def get_is_active(self, obj):
        status = obj.user.is_active
        return status

    def get_username(self, obj):
        username = obj.user.username
        return username
