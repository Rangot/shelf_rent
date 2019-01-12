from django.contrib import admin
from django.db import models
# from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.templatetags.admin_list import _boolean_icon
from .models import *


class ShelfAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']

    class Meta:
        model = Shelf

admin.site.register(Shelf, ShelfAdmin)


class RentsAdmin(admin.ModelAdmin):
    list_display = ['number', 'start_date', 'stop_date', 'tenants', 'term_left']

    exclude = ['updated']

    class Meta:
        model = Rents

admin.site.register(Rents, RentsAdmin)


class ActAdmin(admin.ModelAdmin):
    list_display = ['rents', 'start_date', 'stop_date', 'term', 'term_left', 'payment']
    raw_id_fields = ('shelf', )

    exclude = ['timestamp', 'updated']

    class Meta:
        model = Act

admin.site.register(Act, ActAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_id', 'percent_from_sales', 'rent_of_shelf']

    class Meta:
        model = Category

admin.site.register(Category, CategoryAdmin)