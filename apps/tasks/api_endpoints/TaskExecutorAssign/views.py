from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.tasks.api_endpoints.TaskExecutorAssign.serializers import AssignExecutorSerializer
from apps.tasks.permissions import IsProjectManager


class AssignExecutorAPIView(GenericAPIView):
    serializer_class = AssignExecutorSerializer
    permission_classes = [IsAuthenticated, IsProjectManager]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            task = serializer.validated_data['task']
            user = serializer.validated_data['user']

            task.assignees.add(user)
            return Response({
                "message": f"{user.first_name} {user.last_name} executor sifatida tayinlandi.",
                "task": task.task_title,
                "executor_id": user.id
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


__all__ = [
    "AssignExecutorAPIView"
]
