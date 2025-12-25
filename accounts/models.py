from django.contrib.auth.models import AbstractUser
from django.db import models


class AdminRole(models.TextChoices):
    SUPER_ADMIN = "SUPER_ADMIN", "Super admin"
    STAFF_ADMIN = "STAFF_ADMIN", "Staff admin"
    SUPPORT     = "SUPPORT", "Support"
    VIEW_ONLY   = "VIEW_ONLY", "View only"


class User(AbstractUser):
    """
    Single user model for the whole project.

    - Extends Django's AbstractUser (username, email, password, etc.)
    - Adds 'role' to distinguish admin levels.
    - Still works with Groups and Permissions. [web:58]
    """
    role = models.CharField(
        max_length=20,
        choices=AdminRole.choices,
        default=AdminRole.VIEW_ONLY,
    )

    @property
    def is_super_admin(self):
        return self.role == AdminRole.SUPER_ADMIN

    @property
    def is_staff_admin(self):
        return self.role in {AdminRole.SUPER_ADMIN, AdminRole.STAFF_ADMIN}
