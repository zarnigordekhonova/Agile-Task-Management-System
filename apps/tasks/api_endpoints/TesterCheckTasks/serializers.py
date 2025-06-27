from rest_framework import serializers

from apps.tasks.models import Task, TaskStatus


class TesterVerifyTaskSerializer(serializers.Serializer):
    task_id = serializers.IntegerField()
    action = serializers.ChoiceField(choices=["accept", "reject"])
    comment = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        task_id = attrs['task_id']
        action = attrs['action']
        comment = attrs.get('comment')

        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise serializers.ValidationError("Vazifa topilmadi")

        if task.status != TaskStatus.READY_FOR_TESTING:
            raise serializers.ValidationError("Faqat 'Ready for Testing' holatidagi tasklarni tekshirish mumkin.")

        if action == "reject" and not comment:
            raise serializers.ValidationError("Vazifani rad qilish uchun izoh majburiy.")

        attrs['task'] = task
        return attrs
