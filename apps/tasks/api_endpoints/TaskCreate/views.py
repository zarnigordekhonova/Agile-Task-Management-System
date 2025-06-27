from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.tasks.models import Task
from apps.tasks.task_status import TaskPriority
from apps.tasks.api_endpoints.TaskCreate.serializers import TaskCreateSerializer
from apps.tasks.permissions import IsProjectManager

from apps.notifications.utils import send_notification_email


class TaskCreateAPIView(CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    permission_classes = [IsAuthenticated, IsProjectManager]

    def perform_create(self, serializer):
        task = serializer.save(creator=self.request.user)

        assignee_emails = [user.email for user in task.assignees.all()]
        if assignee_emails:
            send_notification_email(
                subject="New task assigned",
                message=f"New task assigned: '{task.task_title}'",
                recipient_list=assignee_emails
            )

        if task.priority == TaskPriority.HIGH:
            member_emails = [user.email for user in task.project.members.all()]
            if member_emails:
                send_notification_email(
                    subject="URGENT! High-priority task",
                    message=f"URGENT! Task #{task.id} (High): '{task.task_title}'",
                    recipient_list=member_emails
                )


__all__ = [
    "TaskCreateAPIView"
]