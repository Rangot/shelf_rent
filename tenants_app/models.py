from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta
from .utils import CustomBooleanField

from shelf_rent_auth.models import Tenant


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
    tenants = models.ForeignKey(Tenant, related_name='tenant', db_column='tenant', verbose_name='Арендатор',
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
        return str(self.rents_id) + ' (' + str(self.tenants.username) + ')'


class Act(models.Model):
    act_number = models.AutoField(primary_key=True, verbose_name='Номер акта')
    rents = models.ForeignKey('Rents', models.DO_NOTHING, db_column='rents', null=True,
                              verbose_name='Договор')
    shelf = models.OneToOneField('Shelf', models.DO_NOTHING, db_column='shelf', null=True,
                                 verbose_name='Полка')
    category = models.ForeignKey('Category', models.DO_NOTHING, db_column='category',
                                 verbose_name='Категория условий аренды')
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


class Category(models.Model):
    category_id = models.AutoField(primary_key=True, verbose_name='Номер категории')
    percent_from_sales = models.FloatField(max_length=5, default=0, verbose_name='Процент с продаж')
    rent_of_shelf = CustomBooleanField(default=True, verbose_name='Плата за аренду полки')

    class Meta:
        db_table = 'category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return 'процент с продаж - ' + str(self.percent_from_sales) + '%,' + \
               ' плата за аренду - ' + str(self.rent_of_shelf)

#
# class Payment(models.Model):
#     payment_id = models.AutoField(primary_key=True)


class Cash(models.Model):
    id_cash = models.AutoField(primary_key=True)
    cash_date = models.DateTimeField(default=timezone.now, verbose_name='Дата продажи')
    orders = models.ForeignKey('Orders', models.DO_NOTHING, null=True, db_column='orders',
                               verbose_name='Наименование товара')
    sell = models.IntegerField(default=0, verbose_name='Продано')
    all_cash = models.FloatField(max_length=45, default=0, verbose_name='Сумма продажи')
    cash_nal = models.FloatField(max_length=45, default=0, verbose_name='Наличный расчет')
    cash_beznal = models.FloatField(max_length=45, default=0, verbose_name='Безналичный расчет')
    discount = models.FloatField(max_length=45, default=0, verbose_name='Скидка')
    nal = models.BooleanField(default=True)

    # def save(self, **kwargs):
    #     super(Cash, self).save(**kwargs)
    #     self.sell = self.cash_nal + self.cash_beznal
    #     super(Cash, self).save(**kwargs)

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


class Paybox(models.Model):
    slug = models.SlugField
    cash_in_paybox = models.FloatField(max_length=45, default=0, verbose_name='Положили в кассу')
    cash_taken = models.FloatField(max_length=45, default=0, verbose_name='Забрали из кассы')
    cash_remain = models.FloatField(max_length=45, default=0, verbose_name='Денег в кассе')

    def save(self, **kwargs):
        self.cash_remain = self.cash_in_paybox - self.cash_taken
        super(Paybox, self).save(**kwargs)

    class Meta:
        verbose_name = 'Paybox'
