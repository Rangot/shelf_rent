# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError

from tenants_app.models import Tenants, Rents, Act, Orders, Shelf, Cash


class TenantsForm(forms.ModelForm):
    class Meta:
        model = Tenants
        fields = ['name', 'telephone', 'email', 'pass_serial', 'pass_number',
                  'pass_given', 'address']

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


class ActForm(forms.ModelForm):
    class Meta:
        model = Act
        fields = ['rents', 'shelf', 'start_date', 'stop_date', 'payment']

    def __init__(self, *args, **kwargs):
        super(ActForm, self).__init__(*args, **kwargs)
        shelfs_in_use = Act.objects.filter().values('shelf')
        shelfs = Shelf.objects.exclude(shelf_id__in=shelfs_in_use)
        self.fields['shelf'].queryset = shelfs


class ActFormEdit(forms.ModelForm):
    class Meta:
        model = Act
        fields = ['rents', 'shelf', 'start_date', 'stop_date', 'payment']


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
        fields = ['cash_date', 'orders', 'sell', 'discount']


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
