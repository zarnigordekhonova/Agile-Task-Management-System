from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from django.shortcuts import get_object_or_404

from apps.tasks.models import Task
from apps.tasks.task_status import TaskPriority
from apps.notifications.utils import send_notification_email
from apps.tasks.api_endpoints.TaskEdit.serializers import TaskUpdateSerializer
from apps.tasks.permissions import IsProjectManager


class TaskUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskUpdateSerializer
    permission_classes = [IsAuthenticated, IsProjectManager]
    lookup_url_kwarg = 'task_id'

    def get_object(self):
        task = get_object_or_404(Task, id=self.kwargs['task_id'])

        if self.request.user not in task.project.members.all():
            raise PermissionDenied("Sizda bu vazifani tahrirlashga ruxsat yo‘q.")
        return task

    def perform_update(self, serializer):
        task = self.get_object()
        old_priority = task.priority

        updated_task = serializer.save()

        emails = [member.email for member in updated_task.project.members.all()]
        send_notification_email(
            subject="URGENT! High-priority task",
            message=f"URGENT! Task #{updated_task.id} (High): '{updated_task.task_title}'",
            recipient_list=emails
        )


__all__ = [
    "TaskUpdateAPIView"
]