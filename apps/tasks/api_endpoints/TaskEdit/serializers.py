from rest_framework import serializers

from apps.tasks.models import Task


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['task_title', 'description', 'status', 'priority']

    def validate(self, attrs):
        return attrs
