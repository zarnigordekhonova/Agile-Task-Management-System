from rest_framework import serializers

from apps.tasks.models import Task
from apps.tasks.task_status import TaskStatus


class TaskStatusChangeDeveloperSerializer(serializers.Serializer):
    task_id = serializers.IntegerField()
    new_status = serializers.ChoiceField(choices=[
        TaskStatus.TO_DO,
        TaskStatus.IN_PROGRESS,
        TaskStatus.READY_FOR_TESTING
    ])

    def validate(self, attrs):
        task_id = attrs['task_id']
        new_status = attrs['new_status']

        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise serializers.ValidationError("Vazifa topilmadi")

        current_status = task.status
        allowed_transitions = {
            TaskStatus.BACKLOG: TaskStatus.TO_DO,
            TaskStatus.TO_DO: TaskStatus.IN_PROGRESS,
            TaskStatus.IN_PROGRESS: TaskStatus.READY_FOR_TESTING,
        }


        if current_status not in allowed_transitions or allowed_transitions[current_status] != new_status:
            raise serializers.ValidationError(
                f"{current_status} holatidan {new_status} ga o‘tishga ruxsat yo‘q"
            )

        attrs['task'] = task
        return attrs
