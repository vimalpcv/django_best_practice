from django.db import models
from django.contrib.auth.models import AbstractUser

from common.models import BaseModel
from common.constants import GENDER, MALE, ROLES


class Organization(models.Model):
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
        return f'{self.id}: {self.name}'


class User(AbstractUser):
    """
    Extending User model
    """
    emp_id = models.CharField(max_length=10, null=False, blank=False, unique=True, db_index=True)
    gender = models.CharField(max_length=6, choices=GENDER, default=MALE)
    #avatar = models.ImageField(upload_to='/avatars', blank=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=False)

    class Meta:
        # indexes = [
        #     models.Index(fields=['id'])
        # ]
        ordering = ['-id']

    def __str__(self):
        return f'{self.id}: {self.first_name} {self.last_name}'

