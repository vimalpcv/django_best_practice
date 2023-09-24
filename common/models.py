from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('user.User', on_delete=models.SET_NULL,
                                   related_name="%(class)s_created_by", null=True, blank=False, default=1)
    updated_by = models.ForeignKey('user.User', on_delete=models.SET_NULL,
                                   related_name="%(class)s_updated_by", null=True, blank=False, default=1)

    class Meta:
        abstract = True
