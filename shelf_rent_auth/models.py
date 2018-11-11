from django.contrib.auth.models import AbstractUser
from django.db import models


# class TenantUser(AbstractUser):
#     tenant = models.OneToOneField(
#         'tenants_app.Tenants', null=True, default=None, blank=True, on_delete=models.PROTECT)
