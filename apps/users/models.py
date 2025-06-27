from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from apps.users.managers import CustomUserManager


class Role(models.TextChoices):
    PROJECT_OWNER = 'project_owner', _("Project Owner")
    PROJECT_MANAGER = 'project_manager', _("Project Manager")
    DEVELOPER = "developer", _("Developer")
    TESTER = "tester", _("Tester")
    USER = "user", _("User")


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("Email address"), unique=True)
    first_name = models.CharField(_("First name"), max_length=128)
    last_name = models.CharField(_("Last name"), max_length=128)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return (f"{self.id} | {self.email} | {self.role}")