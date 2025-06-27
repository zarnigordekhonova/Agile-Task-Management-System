from rest_framework import serializers

from apps.tasks.models import Task


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'id',
            'project',
            'task_title',
            'description',
            'status',
            'priority')

    def validate_project(self, value):
        user = self.context['request'].user
        if user not in value.members.all():
            raise serializers.ValidationError("Siz bu project a'zosi emassiz.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        return Task.objects.create(creator=user, **validated_data)
