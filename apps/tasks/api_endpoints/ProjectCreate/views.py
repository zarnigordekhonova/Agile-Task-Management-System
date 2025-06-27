from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.tasks.models import Project
from apps.tasks.permissions import IsAnyRole
from .serializers import ProjectCreateSerializer


class ProjectCreateAPIView(ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectCreateSerializer
    permission_classes = [IsAuthenticated, IsAnyRole]

    def perform_create(self, serializer):
        serializer.save()


__all__ = [
    'ProjectCreateAPIView'
]