from django.contrib.auth.models import AbstractUser
from django.db import models


class Tenant(AbstractUser):
    tenants_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, verbose_name='ФИО')
    telephone = models.CharField(max_length=45, blank=True, null=True, verbose_name='Телефон')
    email = models.EmailField(max_length=45, blank=True, null=True, verbose_name='E-mail')
    pass_serial = models.CharField(max_length=4, blank=True, null=True, verbose_name='Серия паспорта')
    pass_number = models.CharField(max_length=6, blank=True, null=True, verbose_name='Номер паспорта')
    pass_given = models.TextField(max_length=1000, blank=True, null=True, verbose_name='Выдан')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='Адрес')

    class Meta:
        db_table = 'tenants'
        verbose_name = 'Tenant'
        verbose_name_plural = 'Tenant'

    def __str__(self):
        return str(self.username)