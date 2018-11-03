from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta

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
    stop_date = models.DateField(blank=True, null=True, verbose_name='Дата истечения')
    updated = models.DateField(auto_now=True)
    term_left = models.DurationField(blank=True, null=True, editable=False)
    is_active = models.BooleanField(default=True, editable=False)
    is_break = models.BooleanField(default=False, editable=False)
    tenants = models.ForeignKey('Tenants', related_name='tenants', db_column='tenants', verbose_name='Арендатор',
                                on_delete=models.DO_NOTHING)

    def save(self, **kwargs):
        super(Rents, self).save(**kwargs)
        self.stop_date = self.start_date + timedelta(days=365)
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
    payment = models.FloatField(max_length=45, verbose_name='Оплата')
    all_payment = models.FloatField(max_length=45, default=None, blank=True, null=True)
    is_active = models.BooleanField(default=True, editable=False)

    def save(self, **kwargs):
        super(Act, self).save(**kwargs)
        self.term = self.stop_date - self.start_date
        self.term_left = self.stop_date - self.updated
        if self.term_left.days <= 0:
            self.is_active = False
        elif self.term_left.days > 0:
            self.is_active = True
        if not self.all_payment:
            self.all_payment = int(self.payment)
        super(Act, self).save(**kwargs)

    class Meta:
        db_table = 'act'


class Cash(models.Model):
    id_cash = models.AutoField(primary_key=True)
    cash_date = models.DateTimeField(default=timezone.now, verbose_name='Дата продажи')
    orders = models.ForeignKey('Orders', models.DO_NOTHING, null=True, db_column='orders',
                               verbose_name='Наименование товара')
    sell = models.IntegerField(default=0, verbose_name='Продано')
    all_cash = models.FloatField(max_length=45, default=0, verbose_name='Сумма продажи')
    discount = models.FloatField(max_length=45, default=0, verbose_name='Скидка')
    nal = models.BooleanField(default=True)


    class Meta:
        db_table = 'cash'

'''
    def full_clean(self, exclude=None, validate_unique=True):
        raise ValidationError('На полке нет столько товара')
'''


class Orders(models.Model):
    orders_id = models.AutoField(primary_key=True)
    act = models.ForeignKey(Act, models.DO_NOTHING, db_column='act', verbose_name='Номер акта')
    name_item = models.CharField(max_length=45, verbose_name='Наименование')
    description_item = models.CharField(max_length=100, blank=True, null=True, verbose_name='Описание')
    materials = models.CharField(max_length=45, blank=True, null=True, verbose_name='Материалы')
    quality = models.IntegerField(default=0, verbose_name='Количество')
    all_sell = models.IntegerField(default=0, verbose_name='Всего продано')
    all_take = models.IntegerField(default=0, verbose_name='Всего забрал арендатор')
    price = models.FloatField(max_length=45, default=0, verbose_name='Цена')
    is_active = models.BooleanField(default=True, editable=True)

    class Meta:
        db_table = 'orders'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


# class User(AbstractUser):
#     pass
