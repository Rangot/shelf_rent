from django.urls import reverse
from django.db.models import Q
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, FileResponse
from django.shortcuts import render_to_response
from django.template.loader import get_template
# from weasyprint import HTML, CSS
from django.contrib import messages

# from django.views.generic import View
# from .utils import render_to_pdf
# from shelf_rent import settings

from wkhtmltopdf.views import PDFTemplateView, PDFTemplateResponse
import pdfkit
from io import StringIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from cgi import html


from django.template.loader import render_to_string

from tenants_app.models import Tenants, Rents, Act, Orders, Shelf, Cash
from tenants_app.forms import TenantsForm, RentsForm, ActForm, OrderForm, ShelfForm, CashForm


def index(request):
    rents_expire = []
    if request.method == 'GET':
        rents = Rents.objects.filter(is_active=True)
        for rent in rents:
            rent.save()
            if 0 < rent.term_left.days < 10:
                rents_expire.append(rent)
        tenants = Tenants.objects.order_by('name')
        return render(request, 'tenants_app/index.html', {'tenants': tenants,
                                                          'rents': rents_expire})
    return HttpResponse(status=405)


def create(request):
    if request.method == 'GET':
        c = {
            'tenants_form': TenantsForm(),
        }
        return render(request, 'tenants_app/create.html', c)

    elif request.method == 'POST':
        tenants_form = TenantsForm(request.POST)

        if tenants_form.is_valid():
            with transaction.atomic():
                tenant = tenants_form.save()

            return redirect(reverse('tenants:view', kwargs={
                'tenant_id': tenant.pk
            }))
        else:
            c = {
                'tenants_form': TenantsForm(),
            }
            return render(request, 'tenants_app/create.html', c)
    return HttpResponse(status=405)


def edit(request, tenant_id):
    instance = get_object_or_404(Tenants, pk=tenant_id)

    if request.method == "POST":
        tenants_form = TenantsForm(request.POST, instance=instance)

        if tenants_form.is_valid():
            tenant = tenants_form.save(commit=False)
            tenant.instance = instance
            tenant.save()
            return redirect(reverse('tenants:view', kwargs={
                'tenant_id': instance.pk
            }))
        else:
            c = {'tenants_form': TenantsForm(instance=instance), 'instance': instance}
            return render(request, 'tenants_app/edit.html', c)
    else:
        if request.method == 'GET':
            return render(request, 'tenants_app/edit.html',
            {'instance': instance, 'tenants_form': TenantsForm(instance=instance)})

    return HttpResponse(status=405)


def view(request, tenant_id):
    if request.method == 'GET':
        # pizza = get_object_or_404(PizzaOrder, id=pizza_order_id)

        #pizza = PizzaOrder.objects.filter(id=pizza_order_id).first()
        #pizza = PizzaOrder.objects.select_related().filter(id=pizza_order_id).first()
        tenant = Tenants.objects.filter(tenants_id=tenant_id).first()
        rents = Rents.objects.filter(tenants=tenant).order_by('is_active').reverse()
        # pizza = PizzaOrder.objects.select_related()\
        #     .prefetch_related()\
        #     .filter(id=pizza_order_id)\
        #     .first()
        # pizza = PizzaOrder.objects\
        #     .select_related()\
        #     .prefetch_related('extra', 'exclude')\
        #     .filter(id=pizza_order_id).first()

        if not tenant:
            raise Http404

        return render(request, 'tenants_app/view.html', {'tenant': tenant, 'rents': rents})
    return HttpResponse(status=405)


def search(request):
    error = False
    tenants = Tenants.objects.order_by('name')
    template = 'tenants_app/search_results.html'
    if 'q' in request.GET:
        q = request.GET.get('q')
        if not q:
            error = True
        else:
            tenants = Tenants.objects.filter(
                Q(name__icontains=q) | Q(telephone__icontains=q) | Q(email__icontains=q))
            return render_to_response(template, {'tenants': tenants, 'query': q})
    return render(request, 'tenants_app/index.html', {'error': error, 'tenants': tenants})


def create_rent(request, tenant_id):
    if request.method == 'GET':
        instance = Tenants.objects.get(pk=tenant_id)
        form = RentsForm(initial={'tenants': instance})
        c = {'instance': instance, 'rents_form': form}
        return render(request, 'tenants_app/create_rent.html', c)

    elif request.method == 'POST':
        rents_form = RentsForm(request.POST)

        if rents_form.is_valid():
            with transaction.atomic():
                rent = rents_form.save()

            return redirect(reverse('tenants:view_rent', kwargs={
                'rents_id': rent.pk
            }))
        else:
            instance = Tenants.objects.get(pk=tenant_id)
            return render(request, 'tenants_app/create_rent.html',
                          {'instance': instance,
                           'rents_form': RentsForm(initial={'tenants': instance})})


def view_rent(request, rents_id):
    if request.method == 'GET':
        rent = Rents.objects.filter(rents_id=rents_id).first()
        acts = Act.objects.filter(rents=rent).order_by('is_active').reverse()
        print(rent)
        print(acts)
        if not rent:
            raise Http404
        return render(request, 'tenants_app/view_rent.html', {'rent': rent, 'acts': acts})
    return HttpResponse(status=405)


def edit_rent(request, rents_id):
    instance = get_object_or_404(Rents, pk=rents_id)

    if request.method == "POST":
        rent_form = RentsForm(request.POST, instance=instance)

        if rent_form.is_valid():
            rent = rent_form.save(commit=False)
            rent.instance = instance
            rent.save()
            return redirect(reverse('tenants:view_rent', kwargs={
                'rents_id': instance.pk
            }))
        else:
            c = {'rent_form': RentsForm(instance=instance), 'instance': instance}
            return render(request, 'tenants_app/edit_rent.html', c)
    else:
        if request.method == 'GET':
            return render(request, 'tenants_app/edit_rent.html',
                          {'instance': instance, 'rent_form': RentsForm(instance=instance)})

    return HttpResponse(status=405)

# export_to_pdf for windows

def export_to_pdf_rent(request, rents_id):
    rent = Rents.objects.filter(rents_id=rents_id).first()
    acts = Act.objects.filter(rents=rent).filter(is_active=True)
    context = {'rent': rent, 'acts': acts}
    content = ''
    if len(acts) == 1:
        content = render_to_string('tenants_app/contract_pdf_rent.html', context)
    if len(acts) > 1:
        content = render_to_string('tenants_app/contract_pdf_rent_many.html', context)
    pdf = pdfkit.PDFKit(content, 'string').to_pdf()

    response = HttpResponse(pdf)
    response['Content-Type'] = 'application/pdf'
    # 'attachment' instead 'inline' to print
    response['Content-disposition'] = 'inline; filename="print_rent.pdf"'
    return response

'''
# export_to_pdf for linux/python any where
def export_to_pdf_rent(request, rents_id):
    rent = Rents.objects.filter(rents_id=rents_id).first()
    acts = Act.objects.filter(rents=rent).filter(is_active=True)
    context = {'rent': rent, 'acts': acts}
    template = get_template('tenants_app/contract_pdf_rent.html')
    html = template.render(context)
    result = StringIO()

    pdf = pisa.pisaDocument(StringIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
'''

# ReportLab
class InvoicePDFView(PDFTemplateView):
    template_name = "tenants_app/contract_pdf_rent.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rent = Rents.objects.filter(rents_id=context['rents_id']).first()
        acts = Act.objects.filter(rents=rent).filter(is_active=True)
        myinstance = {'rent': rent, 'acts': acts}
        context['myinstance'] = myinstance
        return context


def create_act(request, rents_id):
    if request.method == 'GET':
        instance = Rents.objects.get(pk=rents_id)
        form = ActForm(initial={'rents': instance})
        c = {'instance': instance, 'act_form': form}
        return render(request, 'tenants_app/create_act.html', c)

    elif request.method == 'POST':
        act_form = ActForm(request.POST)

        if act_form.is_valid():
            with transaction.atomic():
                act = act_form.save()

            return redirect(reverse('tenants:view_act', kwargs={
                'act_number': act.pk
            }))
        else:
            instance = Rents.objects.get(pk=rents_id)
            return render(request, 'tenants_app/create_act.html',
                          {'instance': instance,
                           'act_form': ActForm(initial={'rents': instance})})
    return HttpResponse(status=405)


def view_act(request, act_number):
    if request.method == 'GET':
        act = Act.objects.filter(act_number=act_number).first()
        orders = Orders.objects.filter(act=act)
        if not act:
            raise Http404
        return render(request, 'tenants_app/view_act.html', {'act': act, 'orders': orders})
    return HttpResponse(status=405)


def edit_act(request, act_number):
    instance = get_object_or_404(Act, pk=act_number)

    if request.method == "POST":
        act_form = ActForm(request.POST, instance=instance)

        if act_form.is_valid():
            act = act_form.save(commit=False)
            act.instance = instance
            act.save()
            return redirect(reverse('tenants:view_act', kwargs={
                'act_number': instance.pk
            }))
        else:
            c = {'act_form': ActForm(instance=instance), 'instance': instance}
            return render(request, 'tenants_app/edit_act.html', c)
    else:
        if request.method == 'GET':
            return render(request, 'tenants_app/edit_act.html',
            {'instance': instance, 'act_form': ActForm(instance=instance)})

    return HttpResponse(status=405)

# export_to_pdf for windows

def export_to_pdf_act(request, act_number):
    act = Act.objects.filter(act_number=act_number).first()
    orders = Orders.objects.filter(act=act)
    context = {'orders': orders, 'act': act}

    content = render_to_string('tenants_app/contract_pdf_act.html', context)
    pdf = pdfkit.PDFKit(content, 'string').to_pdf()

    response = HttpResponse(pdf)
    response['Content-Type'] = 'application/pdf'
    # 'attachment' instead 'inline' to print
    response['Content-disposition'] = 'inline; filename="print_act.pdf"'
    return response

'''
# export_to_pdf for linux/python any where
def export_to_pdf_act(request, act_number):
    act = Act.objects.filter(act_number=act_number).first()
    orders = Orders.objects.filter(act=act)
    context = {'orders': orders, 'act': act}

    html_string = render_to_string('tenants_app/contract_pdf_act.html', context)
    html = HTML(string=html_string)
    main_doc = html.render()
    result = main_doc.write_pdf()

    response = HttpResponse(result, content_type='application/pdf')
    # 'attachment' instead 'inline' to print
    response['Content-disposition'] = 'inline; filename="print.pdf"'
    return response
'''

def create_order(request, act_number):
    if request.method == 'GET':
        instance = Act.objects.get(pk=act_number)
        form = OrderForm(initial={'act': instance})
        c = {'instance': instance, 'order_form': form}
        return render(request, 'tenants_app/create_order.html', c)

    elif request.method == 'POST':
        order_form = OrderForm(request.POST)

        if order_form.is_valid():
            with transaction.atomic():
                order = order_form.save()

            return redirect(reverse('tenants:view_order', kwargs={
                'orders_id': order.pk
            }))
        else:
            instance = Act.objects.get(pk=act_number)
            return render(request, 'tenants_app/create_order.html',
                          {'instance': instance,
                           'order_form': OrderForm(initial={'act': instance})})
    return HttpResponse(status=405)


def view_order(request, orders_id):
    if request.method == 'GET':
        order = Orders.objects.filter(orders_id=orders_id).first()
        if not order:
            raise Http404
        return render(request, 'tenants_app/view_order.html', {'order': order})
    return HttpResponse(status=405)


def edit_order(request, orders_id):
    instance = get_object_or_404(Orders, pk=orders_id)

    if request.method == "POST":
        order_form = OrderForm(request.POST, instance=instance)

        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.instance = instance
            order.save()
            return redirect(reverse('tenants:view_order', kwargs={
                'orders_id': instance.pk
            }))
        else:
            c = {'order_form': OrderForm(instance=instance), 'instance': instance}
            return render(request, 'tenants_app/edit_order.html', c)
    else:
        if request.method == 'GET':
            return render(request, 'tenants_app/edit_order.html',
                          {'instance': instance, 'order_form': OrderForm(instance=instance)})

    return HttpResponse(status=405)

'''
def delete_order(request, orders_id):
    instance = get_object_or_404(Orders, pk=orders_id)
    act = instance.act
    if request.method == 'GET':
        instance.delete()
        return redirect(reverse('tenants:view_act', kwargs={
            'act_number': act.pk
        }))
    return HttpResponse(status=405)
'''


def sales_ledger(request):
    if request.method == 'GET':
        shelfs = Shelf.objects.all()
        return render(request, 'tenants_app/sales_ledger.html', {'shelfs': shelfs})
    return HttpResponse(status=405)


def create_shelf(request):
    if request.method == 'GET':
        c = {
            'shelf_form': ShelfForm(),
        }
        return render(request, 'tenants_app/create_shelf.html', c)

    elif request.method == 'POST':
        shelf_form = ShelfForm(request.POST)

        if shelf_form.is_valid():
            with transaction.atomic():
                shelf = shelf_form.save()

            return redirect(reverse('tenants:sales_ledger'))
        else:
            c = {
                'shelf_form': ShelfForm(),
            }
            return render(request, 'tenants_app/create_shelf.html', c)
    return HttpResponse(status=405)


def edit_shelf(request, shelf_id):
    instance = get_object_or_404(Shelf, pk=shelf_id)

    if request.method == "POST":
        shelf_form = ShelfForm(request.POST, instance=instance)

        if shelf_form.is_valid():
            shelf = shelf_form.save(commit=False)
            shelf.instance = instance
            shelf.save()
            return redirect(reverse('tenants:sales_ledger'))
        else:
            c = {'shelf_form': ShelfForm(instance=instance), 'instance': instance}
            return render(request, 'tenants_app/edit_shelf.html', c)
    else:
        if request.method == 'GET':
            return render(request, 'tenants_app/edit_shelf.html',
            {'instance': instance, 'shelf_form': ShelfForm(instance=instance)})

    return HttpResponse(status=405)


def view_shelf(request, shelf_id):
    if request.method == 'GET':
        shelf = Shelf.objects.filter(shelf_id=shelf_id).first()
        act = Act.objects.filter(shelf=shelf).first()
        orders = Orders.objects.filter(act=act).filter(is_active=True)
        for order in orders:
            all_sell = 0
            all_take = 0
            cashes = Cash.objects.filter(orders=order)
            for cash in cashes:
                order.quality = int(order.quality) - (int(cash.sell) + int(cash.take))
                all_sell += int(cash.sell)
                all_take += int(cash.take)
            order.all_sell = int(order.all_sell) + all_sell
            order.all_take = int(order.all_take) + all_take
        if not shelf:
            raise Http404
        return render(request, 'tenants_app/view_shelf.html', {'shelf': shelf,
                                                               'act': act, 'orders': orders})
    return HttpResponse(status=405)


def create_cash(request, orders_id):
    if request.method == 'GET':
        instance = Orders.objects.get(pk=orders_id)
        form = CashForm(initial={'orders': instance})
        c = {'instance': instance, 'cash_form': form}
        return render(request, 'tenants_app/create_cash.html', c)

    elif request.method == 'POST':
        cash_form = CashForm(request.POST)

        if cash_form.is_valid():
            with transaction.atomic():
                cash = cash_form.save()

            return redirect(reverse('tenants:view_cash'))
        else:
            instance = Orders.objects.get(pk=orders_id)
            return render(request, 'tenants_app/create_cash.html',
                          {'instance': instance,
                           'cash_form': CashForm(initial={'orders': instance})})
    return HttpResponse(status=405)


def view_cash(request):
    if request.method == 'GET':
        cashes = Cash.objects.all().order_by('cash_date').reverse()
        return render(request, 'tenants_app/view_cash.html', {'cashes': cashes})
    return HttpResponse(status=405)


def edit_cash(request, id_cash):
    instance = get_object_or_404(Cash, pk=id_cash)

    if request.method == "POST":
        cash_form = CashForm(request.POST, instance=instance)

        if cash_form.is_valid():
            cash = cash_form.save(commit=False)
            cash.instance = instance
            cash.save()
            return redirect(reverse('tenants:view_cash'))
        else:
            c = {'cash_form': CashForm(instance=instance), 'instance': instance}
            return render(request, 'tenants_app/edit_cash.html', c)
    else:
        if request.method == 'GET':
            return render(request, 'tenants_app/edit_cash.html',
                          {'instance': instance, 'cash_form': CashForm(instance=instance)})

    return HttpResponse(status=405)


def delete_cash(request, id_cash):
    instance = get_object_or_404(Cash, pk=id_cash)
    if request.method == 'GET':
        instance.delete()
        return redirect(reverse('tenants:view_cash'))
    return HttpResponse(status=405)


'''
# print PDF with wkhtmltopdf
class MyPDF(View):
    filename = None
    template_name = None

    def get(self, request, tenant_id):
        tenant = Tenants.objects.filter(tenants_id=tenant_id).first()
        context = {'tenant': tenant}

        response = PDFTemplateResponse(request=request,
                                       template=self.template_name,
                                       filename=self.filename,
                                       context=context,
                                       show_content_in_browser=True)
        return response

'''