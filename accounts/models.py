from django.contrib.auth.models import AbstractUser
from django.db import models


class AdminRole(models.TextChoices):
    SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"
    ADMIN       = "ADMIN", "Admin"
    STAFF       = "STAFF", "Staff"


class User(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=AdminRole.choices,
        default=AdminRole.STAFF,
    )

    @property
    def is_super_admin(self):
        return self.role == AdminRole.SUPER_ADMIN

    @property
    def is_admin(self):
        return self.role in {AdminRole.SUPER_ADMIN, AdminRole.ADMIN}

    @property
    def is_staff_member(self):
        return self.role in {
            AdminRole.SUPER_ADMIN,
            AdminRole.ADMIN,
            AdminRole.STAFF,
        }
