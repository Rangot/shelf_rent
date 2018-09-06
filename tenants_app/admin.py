from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import Tenants, Shelf, Rents, Act


class TenantsAdmin(admin.ModelAdmin):
    list_display = ['name', 'telephone', 'email', 'pass_serial', 'pass_number',
                    'pass_given', 'address']

    class Meta:
        model = Tenants

admin.site.register(Tenants, TenantsAdmin)


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

    exclude = ['timestamp', 'updated']

    class Meta:
        model = Act

admin.site.register(Act, ActAdmin)