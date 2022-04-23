from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class UserProfileDetailUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "name", "nickname", "phone_number")
        extra_kwargs = {
            "id": {"read_only": True},
            "email": {"read_only": True},
            "phone_number": {"read_only": True},
        }
