from django.urls import path
# from wkhtmltopdf.views import PDFTemplateView

from tenants_app.views import *

app_name = 'tenants_app'

urlpatterns = [
    path('create/', create, name='create'),
    path('create_rent/<int:tenant_id>/', create_rent, name='create_rent'),
    path('create_act/<int:rents_id>/', create_act, name='create_act'),
    path('create_order/<int:act_number>/', create_order, name='create_order'),
    path('create_shelf/', create_shelf, name='create_shelf'),
    path('create_cash/<int:orders_id>/', create_cash, name='create_cash'),
    path('view/<int:tenant_id>/', view, name='view'),
    path('view_act/<int:act_number>/', view_act, name='view_act'),
    path('view_rent/<int:rents_id>/', view_rent, name='view_rent'),
    path('view_order/<int:orders_id>/', view_order, name='view_order'),
    path('view_shelf/<int:shelf_id>/', view_shelf, name='view_shelf'),
    path('view_cash/', view_cash, name='view_cash'),
    path('edit/<int:tenant_id>/', edit, name='edit'),
    path('edit_act/<int:act_number>/', edit_act, name='edit_act'),
    path('edit_act_date/<int:act_number>/', edit_act_date, name='edit_act_date'),
    path('edit_rent/<int:rents_id>/', edit_rent, name='edit_rent'),
    path('end_rent/<int:rents_id>/', end_rent, name='end_rent'),
    path('restart_rent/<int:rents_id>/', restart_rent, name='restart_rent'),
    path('edit_order/<int:orders_id>/', edit_order, name='edit_order'),
    path('edit_shelf/<int:shelf_id>/', edit_shelf, name='edit_shelf'),
    # path('edit_cash/<int:id_cash>/', edit_cash, name='edit_cash'),
    path('delete_cash/<int:id_cash>/', delete_cash, name='delete_cash'),
    # delete сейчас не используется
    # path('delete/<int:tenant_id>/', delete, name='delete'),
    # path('delete_order/<int:orders_id>/', delete_order, name='delete_order'),
    path('search/', search, name='search'),
    path('search_order/', search_order, name='search_order'),
    path('search_cash/<int:pk>/', search_cash, name='search_cash'),
    path('print_rent/<int:rents_id>/', export_to_pdf_rent, name='print_rent'),
    # path('print_rent/<int:rents_id>/', InvoicePDFViewRent.as_view(), name='print_rent'),
    path('print_act/<int:act_number>/', export_to_pdf_act, name='print_act'),
    # path('print_act/<int:act_number>/', InvoicePDFViewAct.as_view(), name='print_act'),
    path('sales_ledger/', sales_ledger, name='sales_ledger'),
]
