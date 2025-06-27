from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from apps.tasks.models import Project
from apps.tasks.permissions import IsProjectOwner
from apps.tasks.api_endpoints.AssignRole.serializer import (AssignRoleSerializer,
                                                            UserRoleSerializer, UserListSerializer)

CustomUser = get_user_model()


class AssignRoleAPIView(GenericAPIView):
    permission_classes = [IsProjectOwner]
    serializer_class = AssignRoleSerializer

    def post(self, request, project_id):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            new_role = serializer.validated_data['role']

            project = get_object_or_404(Project, id=project_id)
            user = get_object_or_404(CustomUser, id=user_id)

            if user not in project.members.all():
                return Response(
                    {"detail": "Bu user ushbu loyihaning a'zosi emas"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            old_role = user.role
            user.role = new_role
            user.save()

            return Response({
                "message": f"{user.first_name} {user.last_name} ning roli '{old_role}' dan '{new_role}' ga o'zgartirildi",
                "user": UserRoleSerializer(user).data,
                "old_role": old_role,
                "new_role": new_role
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersListAPIView(ListAPIView):
    """
    Barcha userlarni ko'rish (faqat Project Owner uchun)
    Rol berish uchun user larni ko'rib chiqoladi
    """
    serializer_class = UserListSerializer
    permission_classes = [IsProjectOwner]

    def get_queryset(self):
        queryset = CustomUser.objects.order_by("id")

        return queryset


__all__ = [
    'AssignRoleAPIView', 'UsersListAPIView'
]