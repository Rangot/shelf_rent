from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

# from shelf_rent_auth.models import TenantUser


# class CustomAdminModel(UserAdmin):
#     fieldsets = UserAdmin.fieldsets + (
#         (None, {'fields': ('tenant',)}),
#     )
#     list_display = (
#         'username',
#         'first_name',
#         'last_name',
#         'tenant',
#     )
#     list_editable = (
#         'tenant',
#     )
#     list_filter = (
#         'tenant__name',
#     )
#     list_select_related = ('tenant', )
#     search_fields = (
#         'first_name',
#         'last_name',
#         'tenant__name',
#     )
#
# admin.site.register(TenantUser, CustomAdminModel)
