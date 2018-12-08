# -*- coding: utf-8 -*-

from dal import autocomplete
from django import forms
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render_to_response, HttpResponse
from django.core.exceptions import ValidationError
from ajax_select.fields import AutoCompleteSelectField, AutoCompleteSelectMultipleField

from tenants_app.models import Rents, Act, Orders, Shelf, Cash
from shelf_rent_auth.models import Tenant

# def clean_email(self):
#     email = self.cleaned_data.get('email')
#     email_base, provider = email.split('@')
#     domain, extension = provider.split('.')
#     if not extension == 'com':
#         raise forms.ValidationError('Введите правильный адрес почты')
#     return email


class RentsForm(forms.ModelForm):
    class Meta:
        model = Rents
        fields = ['start_date', 'stop_date', 'tenants']

# создание акта с выпадающим меню полок с исключением занятых
# class ActForm(forms.ModelForm):
#     class Meta:
#         model = Act
#         fields = ['rents', 'shelf', 'start_date', 'stop_date', 'payment']
#
#     def __init__(self, *args, **kwargs):
#         super(ActForm, self).__init__(*args, **kwargs)
#         shelfs_in_use = Act.objects.filter().values('shelf')
#         shelfs = Shelf.objects.exclude(shelf_id__in=shelfs_in_use)
#         self.fields['shelf'].queryset = shelfs


class ActFormEdit(forms.ModelForm):
    class Meta:
        model = Act
        fields = ['rents', 'start_date', 'stop_date', 'payment', 'category']


class ActForm(forms.ModelForm):
    shelf = forms.ModelChoiceField(
        queryset=Shelf.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='shelf_autocomplete',
            attrs={
                # 'data-theme': 'classic',
                'data-placeholder': 'Начните ввод...',
                'data-minimum-input-length': 2,
                # 'data-width': 'style',
                # 'data-language': 'ru'
            })
        )

    def save(self, commit=True):
        shelf_name = self.cleaned_data['shelf']
        if Act.objects.filter(shelf__name__icontains=shelf_name).exists():
            raise forms.ValidationError('Полка уже занята')
        shelf = Shelf.objects.filter(name=shelf_name).first()
        if not shelf:
            raise forms.ValidationError('Такой полки не существует')
        else:
            self.instance.shelf = shelf
            return super(ActForm, self).save(commit)

    class Meta:
        model = Act
        fields = ['rents', 'start_date', 'stop_date', 'payment', 'category']

        # shelfs_in_use = Act.objects.filter().values('shelf')
        # print(shelfs_in_use)
        # for shelf in shelfs_in_use:
        #     if shelf == shelf_name:
        #         return forms.ValidationError('Эта полка уже используется')
        # try:
        #     shelf_name = self.cleaned_data['shelf']
        #     shelf = Shelf.objects.filter(name=shelf_name)[
        #         0]  # returns (instance, <created?-boolean>)
        #     self.instance.shelf = shelf
        #     return super(ActFormEdit, self).save(commit)
        # except IntegrityError:
        #     return HttpResponse('Эта полка уже используется')


class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['act', 'name_item', 'description_item', 'materials', 'quality', 'price', 'is_active']


class ShelfForm(forms.ModelForm):
    class Meta:
        model = Shelf
        fields = ['name', 'price']


class CashForm(forms.ModelForm):
    class Meta:
        model = Cash
        fields = ['cash_date', 'orders', 'sell', 'cash_nal', 'cash_beznal', 'discount']


'''
class PizzaOrderForm(forms.ModelForm):
    class Meta:
        model = PizzaOrder
        exclude = [
            'delivered',
            'date_created',
            'date_delivered',
            'delivery',
        ]

    def clean(self):
        data = self.cleaned_data
        excluded = data['exclude']

        errors = []
        for item in excluded:
            if item in data['extra']:
                errors.append(str(item))

        if errors:
            raise ValidationError(
                'Ingredients [{}] are in extras and excludes!'.format(
                    ', '.join(errors)
                )
            )
        return data

    def save(self, commit=True, delivery=None):
        if delivery is None:
            raise ValueError('Delivery was not set')

        inst = super().save(commit=False)
        inst.delivery = delivery

        if commit:
            inst.save()

        return inst
'''
