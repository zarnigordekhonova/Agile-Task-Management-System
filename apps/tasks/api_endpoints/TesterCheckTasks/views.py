from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.tasks.permissions import IsTester
from apps.tasks.task_status import TaskStatus
from apps.notifications.utils import send_notification_email
from apps.tasks.api_endpoints.TesterCheckTasks.serializers import TesterVerifyTaskSerializer


class TesterVerifyTaskAPIView(GenericAPIView):
    serializer_class = TesterVerifyTaskSerializer
    permission_classes = [IsAuthenticated, IsTester]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            task = serializer.validated_data['task']
            action = serializer.validated_data['action']
            comment = serializer.validated_data.get('comment', "")

            if action == "accept":
                task.status = TaskStatus.DONE
                task.rejection_comment = ""
                task.save()
                return Response({
                    "message": f"Task #{task.id} muvaffaqiyatli qabul qilindi. Holati: Done"
                }, status=status.HTTP_200_OK)

            elif action == "reject":
                task.status = TaskStatus.TO_DO
                task.rejection_comment = comment
                task.save()

                developers = task.assignees.filter(role='developer')
                for dev in developers:
                    send_notification_email(
                        subject="Task rejected",
                        message=f"Task #{task.id} rejected: '{comment}'",
                        recipient_list=[dev.email]
                    )

                return Response({
                    "message": f"Task #{task.id} rad etildi. Holati To Do ga qaytdi.",
                    "reason": comment
                }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


__all__ = [
    'TesterVerifyTaskAPIView'
]
