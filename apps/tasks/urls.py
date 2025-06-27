from django.urls import path
from apps.tasks.api_endpoints import (
    AssignRoleAPIView,
    UsersListAPIView,
    ProjectCreateAPIView,
    AddProjectMemberAPIView,
    ProjectDeleteAPIView,
    TaskCreateAPIView,
    TaskUpdateAPIView,
    AssignExecutorAPIView,
    TaskStatusChangeDeveloperAPIView,
    TesterVerifyTaskAPIView

)

app_name = "tasks"

urlpatterns = [
    path("users-list/", UsersListAPIView.as_view(), name="users-list"),
    path("project-create/", ProjectCreateAPIView.as_view(), name="project-create"),
    path("project/<int:project_id>/add-member/", AddProjectMemberAPIView.as_view(), name="add-project-member"),
    path("project/<int:project_id>/assign-role/", AssignRoleAPIView.as_view(), name="assign-role"),
    path("project/<int:project_id>/delete/", ProjectDeleteAPIView.as_view(), name="delete-project"),
    path("task-create/", TaskCreateAPIView.as_view(), name="task-create"),
    path("task/<int:task_id>/update/", TaskUpdateAPIView.as_view(), name="task-update"),
    path("assign-executor/", AssignExecutorAPIView.as_view(), name="assign-executor"),
    path("task-status-change/", TaskStatusChangeDeveloperAPIView.as_view(), name="task-status-change"),
    path("task-verify/", TesterVerifyTaskAPIView.as_view(), name="task-verify"),
]