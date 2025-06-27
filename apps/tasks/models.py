from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from apps.common.models import BaseModel
from .task_status import TaskStatus, TaskPriority

CustomUser = get_user_model()


class Project(BaseModel):
    project_title = models.CharField(_("Project Name"), max_length=255)
    description = models.TextField(_("Description"))
    owner = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='owned_projects'
    )
    members = models.ManyToManyField(
        CustomUser,
        related_name='projects',
        verbose_name=_("Members"),
        blank=True,
    )

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")

    def __str__(self):
        return self.project_title


class Task(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    task_title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_("Description"))

    assignees = models.ManyToManyField(
        CustomUser,
        related_name="assigned_tasks",
        verbose_name=_("Assignees"),
        blank=True
    )

    status = models.CharField(max_length=30, choices=TaskStatus.CHOICES, default=TaskStatus.BACKLOG)

    priority = models.CharField(max_length=10, choices=TaskPriority.CHOICES, default=TaskPriority.LOW)

    rejection_comment = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")

    def is_high_priority(self):
        return self.priority == TaskPriority.HIGH

    def __str__(self):
        return f"{self.task_title} | ({self.status} | {self.priority})"


class TaskAssignee(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    assignee = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Task Assignee")
        verbose_name_plural = _("Task Assignees")

    def __str__(self):
        return f"{self.task} - {self.assignee.email}"


class TaskHistory(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="history")
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    action = models.TextField(_("Action"))
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Task History")
        verbose_name_plural = _("Task Histories")

    def __str__(self):
        return f"({self.timestamp}) | {self.user} | {self.action}"


class Group(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(
        CustomUser, verbose_name=_("Members"), related_name="chat_groups", blank=True
    )

    class Meta:
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")

    def __str__(self):
        return self.name


class Notification(models.Model):
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")


