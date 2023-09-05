from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('user.User', on_delete=models.SET_NULL,
                                   related_name="%(class)_created_by", null=True, blank=False)
    updated_by = models.ForeignKey('user.User', on_delete=models.SET_NULL,
                                   related_name="%(class)_updated_by", null=True, blank=False)

    class Meta:
        abstract = True