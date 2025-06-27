from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from apps.tasks.models import Project
from apps.tasks.permissions import IsProjectOwner


class ProjectDeleteAPIView(DestroyAPIView):
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated, IsProjectOwner]

    def get_object(self):
        return Project.objects.get(id=self.kwargs['project_id'])


__all__ = [
    "ProjectDeleteAPIView"
]