from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from base.models import BaseModel
from base.constants import GENDER, MALE, ROLES


class Organization(BaseModel):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        default_permissions = ('add', 'change')  # by default add, change, delete
        # db_table = 'custom_table_name'
        # db_table_comment = "custom_table_documentation"
        ordering = ['-id']
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'

    def __str__(self):
        return f'{self.name} ({self.id})'


class User(AbstractUser):
    """
    Custom User model with email as unique field.
    """
    email = models.EmailField(max_length=100, unique=True, null=False, blank=False)
    gender = models.CharField(max_length=6, choices=GENDER, default=MALE)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, null=True, blank=False)
    role = models.CharField(max_length=15, choices=ROLES, default='user')

    class Meta:
        indexes = [
            models.Index(fields=['role'], name='role_idx'),
            models.Index(fields=['organization'], name='organization_idx'),
        ]
        ordering = ['-id']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'user'

    def __str__(self):
        return f'{self.email} ({self.id})'

