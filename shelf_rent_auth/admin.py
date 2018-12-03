from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from shelf_rent_auth.models import Tenant


class CustomAdminModel(UserAdmin):
    # fieldsets = UserAdmin.fieldsets\
    #     ((None, {'fields': ('name', 'telephone', 'email', 'pass_serial', 'pass_number', 'pass_given', 'address')}),
    # )
    list_display = (
        'username',
        'first_name',
        'last_name',
    )
    search_fields = (
        'first_name',
        'last_name',
    )

admin.site.register(Tenant, CustomAdminModel)
