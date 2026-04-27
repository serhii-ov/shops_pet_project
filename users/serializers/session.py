from rest_framework import serializers
from users.models import UserSession


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSession
        fields = [
            "id",
            "user_agent",
            "ip_address",
            "created_at",
            "last_used_at",
        ]
