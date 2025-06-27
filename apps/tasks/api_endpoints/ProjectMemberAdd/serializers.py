from rest_framework import serializers
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class AddProjectMemberSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    def validate_user_id(self, value):
        if not CustomUser.objects.filter(id=value).exists():
            raise serializers.ValidationError("User not found.")
        return value
