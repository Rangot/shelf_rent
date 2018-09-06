from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
# from datetime import *

from django.contrib.auth.models import AbstractUser


class Tenants(models.Model):
    tenants_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, blank=True, null=True, verbose_name='ФИО')
    telephone = models.CharField(max_length=45, blank=True, null=True, verbose_name='Телефон')
    email = models.EmailField(max_length=45, blank=True, null=True, verbose_name='E-mail')
    pass_serial = models.CharField(max_length=4, blank=True, null=True, verbose_name='Серия паспорта')
    pass_number = models.CharField(max_length=6, blank=True, null=True, verbose_name='Номер паспорта')
    pass_given = models.TextField(max_length=1000, blank=True, null=True, verbose_name='Выдан')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='Адрес')

    class Meta:
        db_table = 'tenants'
        verbose_name = 'Tenant'
        verbose_name_plural = 'Tenants'

    def __str__(self):
        return str(self.name)


class Shelf(models.Model):
    shelf_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, unique=True)
    price = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'shelf'

    def __str__(self):
        return str(self.name)


class Rents(models.Model):
    rents_id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=45, blank=True, null=True, unique=True, verbose_name='Номер договора')
    start_date = models.DateField(default=timezone.now, verbose_name='Дата заключения')
    stop_date = models.DateField(verbose_name='Дата истечения')
    updated = models.DateField(auto_now=True)
    term_left = models.DurationField(blank=True, null=True, editable=False)
    is_active = models.BooleanField(default=True, editable=False)
    tenants = models.ForeignKey('Tenants', related_name='tenants', db_column='tenants', verbose_name='Арендатор',
                                on_delete=models.DO_NOTHING)

    def save(self, **kwargs):
        super(Rents, self).save(**kwargs)
        self.term_left = self.stop_date - self.updated
        if self.term_left.days <= 0:
            self.is_active = False
        elif self.term_left.days > 0:
            self.is_active = True
        super(Rents, self).save(**kwargs)

    class Meta:
        db_table = 'rents'
        verbose_name = 'Rent'
        verbose_name_plural = 'Rents'

    def __str__(self):
        return str(self.rents_id) + ' (' + str(self.tenants.name) + ')'


class Act(models.Model):
    act_number = models.AutoField(primary_key=True, verbose_name='Номер акта')
    rents = models.ForeignKey('Rents', models.DO_NOTHING, db_column='rents', null=True,
                              verbose_name='Договор')
    shelf = models.OneToOneField('Shelf', models.DO_NOTHING, db_column='shelf', null=True,
                                 verbose_name='Полка')
    start_date = models.DateField(default=timezone.now, verbose_name='Дата заключения')
    stop_date = models.DateField(verbose_name='Дата истечения')
    timestamp = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    term = models.DurationField(blank=True, null=True, editable=False)
    term_left = models.DurationField(blank=True, null=True, editable=False)
    payment = models.CharField(max_length=45, blank=True, null=True, verbose_name='Оплата')
    is_active = models.BooleanField(default=True, editable=False)

    def save(self, **kwargs):
        super(Act, self).save(**kwargs)
        self.term = self.stop_date - self.start_date
        self.term_left = self.stop_date - self.updated
        if self.term_left.days <= 0:
            self.is_active = False
        elif self.term_left.days > 0:
            self.is_active = True
        super(Act, self).save(**kwargs)

    class Meta:
        db_table = 'act'


class Cash(models.Model):
    id_cash = models.AutoField(primary_key=True)
    cash_date = models.DateTimeField(default=timezone.now, verbose_name='Дата продажи')
    orders = models.ForeignKey('Orders', models.DO_NOTHING, null=True, db_column='orders',
                               verbose_name='Наименование товара')
    sell = models.CharField(max_length=45, default=0, verbose_name='Продано')
    take = models.CharField(max_length=45, default=0, verbose_name='Забрал арендатор')
    discount = models.CharField(max_length=45, blank=True, null=True, verbose_name='Скидка')

    class Meta:
        db_table = 'cash'

'''
    def full_clean(self, exclude=None, validate_unique=True):
        raise ValidationError('На полке нет столько товара')
'''


class Orders(models.Model):
    orders_id = models.AutoField(primary_key=True)
    act = models.ForeignKey(Act, models.DO_NOTHING, db_column='act', verbose_name='Номер акта')
    name_item = models.CharField(max_length=45, blank=True, null=True, verbose_name='Наименование')
    description_item = models.CharField(max_length=100, blank=True, null=True, verbose_name='Описание')
    materials = models.CharField(max_length=45, blank=True, null=True, verbose_name='Материалы')
    quality = models.CharField(max_length=45, default=0, verbose_name='Количество')
    all_sell = models.CharField(max_length=45, default=0, verbose_name='Всего продано')
    all_take = models.CharField(max_length=45, default=0, verbose_name='Всего забрал арендатор')
    price = models.CharField(max_length=45, blank=True, null=True, verbose_name='Цена')
    is_active = models.BooleanField(default=True, editable=True)

    class Meta:
        db_table = 'orders'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


# class User(AbstractUser):
#     pass
