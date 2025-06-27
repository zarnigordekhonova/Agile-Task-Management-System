from rest_framework import serializers

from django.contrib.auth import get_user_model

from apps.tasks.models import Project
from apps.users.models import Role


CustomUser = get_user_model()


class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'project_title', 'description']

    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        if user.role != Role.PROJECT_OWNER:
            user.role = Role.PROJECT_OWNER
            user.save()

        project = Project.objects.create(owner=user, **validated_data)

        project.members.set([user])
        project.save()

        return project

