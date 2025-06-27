from rest_framework import serializers

from django.contrib.auth import get_user_model

from apps.tasks.models import Task

CustomUser = get_user_model()


class AssignExecutorSerializer(serializers.Serializer):
    task_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    def validate(self, attrs):
        task_id = attrs.get('task_id')
        user_id = attrs.get('user_id')

        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise serializers.ValidationError("Vazifa topilmadi.")

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Foydalanuvchi topilmadi.")

        if user not in task.project.members.all():
            raise serializers.ValidationError("Foydalanuvchi bu project a'zosi emas.")

        if user.role not in ['project_manager', 'developer']:
            raise serializers.ValidationError("Foydalanuvchi vazifa bajaruvchisi bo‘la olmaydi. Faqat developer yoki project_manager bo‘lishi kerak.")

        attrs['task'] = task
        attrs['user'] = user
        return attrs
