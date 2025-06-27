from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from django.shortcuts import get_object_or_404

from apps.tasks.models import Project
from apps.tasks.api_endpoints.ProjectMemberAdd.serializers import AddProjectMemberSerializer
from apps.tasks.permissions import IsProjectOwner, IsProjectManager
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class AddProjectMemberAPIView(GenericAPIView):
    permission_classes = [IsProjectOwner]

    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        serializer = AddProjectMemberSerializer(data=request.data)

        if serializer.is_valid():
            user_id = serializer.validated_data["user_id"]
            user = get_object_or_404(CustomUser, id=user_id)

            if user in project.members.all():
                return Response(
                    {"detail": "User is already a member of this project."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            project.members.add(user)

            return Response({
                "message": f"{user.first_name} {user.last_name} added to project '{project.project_title}'"
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


__all__ = [
    'AddProjectMemberAPIView'
]