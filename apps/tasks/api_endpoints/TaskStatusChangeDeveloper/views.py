from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from apps.tasks.permissions import IsDeveloper
from apps.notifications.utils import send_notification_email
from apps.tasks.api_endpoints.TaskStatusChangeDeveloper.serializers import TaskStatusChangeDeveloperSerializer


class TaskStatusChangeDeveloperAPIView(GenericAPIView):
    serializer_class = TaskStatusChangeDeveloperSerializer
    permission_classes = [IsAuthenticated, IsDeveloper]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            task = serializer.validated_data['task']
            new_status = serializer.validated_data['new_status']

            old_status = task.status
            task.status = new_status
            task.save()

            if new_status == "in_progress":
                send_notification_email(
                    subject="Task in progress",
                    message=f"Task #{task.id} in progress (Developer: {request.user.first_name})",
                    recipient_list=[task.project.owner.email]
                )

            elif new_status == "ready_for_testing":
                testers = task.project.members.filter(role='tester')
                for tester in testers:
                    send_email_async(
                        subject="Task awaiting review",
                        message=f"Task #{task.id} awaiting review",
                        recipient_list = [tester.email]
                    )

            return Response({
                "message": f"Task #{task.id} statusi {old_status} dan {new_status} ga o‘zgartirildi"
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
