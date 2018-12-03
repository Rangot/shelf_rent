# -*- coding: utf-8 -*-
from django import forms

from django.contrib.auth.forms import UserCreationForm

from shelf_rent_auth.models import Tenant


class CustomCreationForm(UserCreationForm):
    class Meta:
        model = Tenant
        fields = ('username', 'name', 'telephone', 'email', 'pass_serial', 'pass_number',
                  'pass_given', 'address')
