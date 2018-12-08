from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import Shelf, Rents, Act


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