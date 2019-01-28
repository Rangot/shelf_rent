from django.urls import reverse
from django.db.models import Q
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required, permission_required
# from dal import autocomplete
# from django.contrib.auth import update_session_auth_hash
# from django.shortcuts import render_to_response
# from django.template.loader import get_template
# from django.utils.timezone import datetime
from datetime import datetime, timedelta
import pytz

# from weasyprint import HTML, CSS
# from django.contrib import messages

# from django.views.generic import View
# from .utils import render_to_pdf
# from shelf_rent import settings

# import pdfkit
# from io import StringIO
# from xhtml2pdf import pisa
# from django.template.loader import get_template
# from django.template import Context
# from django.http import HttpResponse
# from cgi import html

# from django.template.loader import render_to_string
# from django.core.paginator import Paginator

from tenants_app.models import *
from tenants_app.forms import *
from shelf_rent_auth.forms import *
from tenants_app.utils import PaginatorMixin


@login_required
def index(request):
    acts_expire = []
    if request.method == 'GET':
        query_acts = []
        rents = Rents.objects.filter(is_active=True, is_break=False)
        for rent in rents:
            act = Act.objects.filter(rents=rent)
            if act:
                query_acts.append(act)
        for acts in query_acts:
            for act in acts:
                act.save()
                if 0 < act.term_left.days < 4:
                    acts_expire.append(act)
        tenants = Tenant.objects.order_by('username').exclude(is_staff=True)

        pagin = PaginatorMixin(request, model=tenants, elements_on_page=10)

        context = {
            'page_object': pagin.page,
            'is_paginated': pagin.is_paginated,
            'next_url': pagin.next_url,
            'prev_url': pagin.prev_url,
            'acts': acts_expire
        }

        return render(request, 'tenants_app/index.html', context)
    return HttpResponse(status=405)


@login_required
@permission_required('Can add Tenant', raise_exception=True)
def create(request):
    if request.method == 'GET':
        c = {
            'tenants_form': CustomCreationForm(),
        }
        return render(request, 'tenants_app/create.html', c)

    elif request.method == 'POST':
        tenants_form = CustomCreationForm(request.POST)

        if tenants_form.is_valid():
            with transaction.atomic():
                tenant = tenants_form.save()

            return redirect(reverse('tenants:view_tenant', kwargs={
                'username': tenant.username
            }))
        else:
            c = {
                'tenants_form': CustomCreationForm(),
            }
            return render(request, 'tenants_app/create.html', c)
    return HttpResponse(status=405)


@login_required
def edit(request):
    instance = get_object_or_404(Tenant, username=request.user.username)

    if request.method == "POST":
        tenants_form = CustomCreationForm(request.POST, instance=instance)

        if tenants_form.is_valid():
            tenant = tenants_form.save(commit=False)
            tenant.instance = instance
            tenant.save()
            return redirect(reverse('tenants:view'))
        else:
            c = {'tenants_form': CustomCreationForm(instance=instance), 'instance': instance}
            return render(request, 'tenants_app/edit.html', c)
    else:
        if request.method == 'GET':
            return render(request, 'tenants_app/edit.html',
                          {'instance': instance, 'tenants_form': CustomCreationForm(instance=instance)})

    return HttpResponse(status=405)


@login_required
@permission_required('Can change Tenant', raise_exception=True)
def edit_tenant(request, username):
    instance = get_object_or_404(Tenant, username=username)

    if request.method == "POST":
        tenants_form = CustomCreationForm(request.POST, instance=instance)

        if tenants_form.is_valid():
            tenant = tenants_form.save(commit=False)
            tenant.instance = instance
            tenant.save()
            return redirect(reverse('tenants:view', kwargs={
                'username': tenant.username
            }))
        else:
            c = {'tenants_form': CustomCreationForm(instance=instance), 'instance': instance}
            return render(request, 'tenants_app/edit.html', c)
    else:
        if request.method == 'GET':
            return render(request, 'tenants_app/edit.html',
                          {'instance': instance, 'tenants_form': CustomCreationForm(instance=instance)})

    return HttpResponse(status=405)


@login_required
def view(request):
    if not request.user.is_staff:
        tenant = get_object_or_404(Tenant, username=request.user.username)
        rents = Rents.objects.filter(tenants=tenant).order_by('is_active').reverse()

        if not tenant:
            raise Http404

        return render(request, 'tenants_app/view.html', {'tenant': tenant, 'rents': rents})
    elif request.user.is_superuser:
        return redirect(reverse('admin:index'))
    else:
        return redirect(reverse('index'))


@login_required
@permission_required('Can view Tenant', raise_exception=True)
def view_tenant(request, username):
    if request.method == 'GET':
        tenant = get_object_or_404(Tenant, username=username)
        rents = Rents.objects.filter(tenants=tenant).order_by('is_active').reverse()

        if not tenant:
            raise Http404

        return render(request, 'tenants_app/view.html', {'tenant': tenant, 'rents': rents})
    return HttpResponse(status=405)


@login_required
def search(request):
    error = False
    tenants = Tenant.objects.order_by('name').exclude(is_staff=True)
    template = 'tenants_app/search_results.html'
    if 'q' in request.GET:
        q = request.GET.get('q')
        if not q:
            error = True
        else:
            tenants = Tenant.objects.filter(
                Q(name__icontains=q) | Q(telephone__icontains=q) | Q(email__icontains=q)).exclude(is_staff=True)

            pagin = PaginatorMixin(request, model=tenants, elements_on_page=10)

            context = {
                'page_object': pagin.page,
                'is_paginated': pagin.is_paginated,
                'next_url': pagin.next_url,
                'prev_url': pagin.prev_url,
                'query': q
            }

            return render_to_response(template, context)
    return render(request, 'tenants_app/index.html', {'error': error, 'tenants': tenants})


def create_rent(request, tenant_id):
    if request.method == 'GET':
        instance = Tenant.objects.get(pk=tenant_id)
        form = RentsForm(initial={'tenants': instance})
        c = {'instance': instance, 'rents_form': form}
        return render(request, 'tenants_app/create_rent.html', c)

    elif request.method == 'POST':
        rents_form = RentsForm(request.POST)

        if rents_form.is_valid():
            with transaction.atomic():
                count_rents = Rents.objects.filter(tenants=tenant_id).filter(is_active=True).count()
                if count_rents == 0:
                    rent = rents_form.save()
                else:
                    return HttpResponse('Нельзя создать ещё один действующий договор')

            return redirect(reverse('tenants:view_rent', kwargs={
                'rents_id': rent.pk
            }))
        else:
            instance = Tenant.objects.get(pk=tenant_id)
            return render(request, 'tenants_app/create_rent.html',
                          {'instance': instance,
                           'rents_form': RentsForm(initial={'tenants': instance})})


def view_rent(request, rents_id):
    if request.method == 'GET':
        rent = Rents.objects.filter(rents_id=rents_id).first()
        acts = Act.objects.filter(rents=rent).order_by('is_active').reverse()
        if not rent:
            raise Http404
        return render(request, 'tenants_app/view_rent.html', {'rent': rent, 'acts': acts})
    return HttpResponse(status=405)


def edit_rent(request, rents_id):
    instance = get_object_or_404(Rents, pk=rents_id)

    if request.method == "POST":
        rent_form = RentsForm(request.POST, instance=instance)

        if rent_form.is_valid():
            tenant_id = instance.tenants_id
            count_rents = Rents.objects.filter(tenants=tenant_id).filter(is_active=True).count()
            if count_rents == 0:
                rent = rent_form.save(commit=False)
                rent.instance = instance
                rent.save()
            else:
                return HttpResponse('Нельзя продлить договор пока есть действующий')
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


def end_rent(request, rents_id):
    rent = Rents.objects.filter(rents_id=rents_id).first()
    rent.is_break = True
    rent.save()
    return redirect(reverse('tenants:view_rent', kwargs={
        'rents_id': rent.pk
    }))


def restart_rent(request, rents_id):
    rent = Rents.objects.filter(rents_id=rents_id).first()
    rent.is_break = False
    rent.save()
    return redirect(reverse('tenants:view_rent', kwargs={
        'rents_id': rent.pk
    }))


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

            return redirect(reverse('tenants:create_order', kwargs={
                'act_number': act.pk
            }))
        else:
            instance = Rents.objects.get(pk=rents_id)
            return render(request, 'tenants_app/create_act.html',
                          {'instance': instance,
                           'act_form': ActForm(initial={'rents': instance})})
    return HttpResponse(status=405)


def view_act(request, act_number):
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
            return redirect(reverse('tenants:view_act', kwargs={
                'act_number': instance.pk
            }))
    else:
        if request.method == 'GET':
            act = Act.objects.filter(act_number=act_number).first()
            orders = Orders.objects.filter(act=act)
            if not act:
                raise Http404
            return render(request, 'tenants_app/view_act.html',
                          {'act': act,
                           'orders': orders,
                           'instance': instance,
                           'act_form': ActForm(instance=instance)
                           })

    return HttpResponse(status=405)


def edit_act(request, act_number):
    instance = get_object_or_404(Act, pk=act_number)

    if request.method == "POST":
        act_form = ActFormEdit(request.POST, instance=instance)
        act_form.shelf = instance.shelf

        if act_form.is_valid():
            act = act_form.save(commit=False)
            act.instance = instance
            act.save()
            return redirect(reverse('tenants:view_act', kwargs={
                'act_number': instance.pk
            }))
        else:
            c = {'act_form': ActFormEdit(instance=instance), 'instance': instance}
            return render(request, 'tenants_app/edit_act.html', c)
    else:
        if request.method == 'GET':
            return render(request, 'tenants_app/edit_act.html',
            {'instance': instance, 'act_form': ActFormEdit(instance=instance)})

    return HttpResponse(status=405)


def edit_act_date(request, act_number):
    instance = get_object_or_404(Act, pk=act_number)

    if request.method == "POST":
        act_form = ActFormEdit(request.POST, instance=instance)

        if act_form.is_valid():
            act = act_form.save(commit=False)
            act.instance = instance
            act.all_payment = float(act.all_payment) + float(act.payment)
            act.save()
            return redirect(reverse('tenants:view_act', kwargs={
                'act_number': instance.pk
            }))
        else:
            c = {'act_form': ActFormEdit(instance=instance), 'instance': instance}
            return render(request, 'tenants_app/edit_act_date.html', c)
    else:
        if request.method == 'GET':
            return render(request, 'tenants_app/edit_act_date.html',
            {'instance': instance, 'act_form': ActFormEdit(instance=instance)})

    return HttpResponse(status=405)


def delete_act_shelf(request, act_number):
    act = Act.objects.filter(act_number=act_number).first()
    act.shelf = None
    act.save()
    return redirect(reverse('tenants:view_act', kwargs={
        'act_number': act.pk
    }))


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


@login_required
def sales_ledger(request):
    if request.method == 'GET':
        shelfs = Shelf.objects.all()
        return render(request, 'tenants_app/sales_ledger.html', {'shelfs': shelfs})
    return HttpResponse(status=405)


@login_required
def search_order(request):
    error = False
    orders = Orders.objects.order_by('name_item')
    template = 'tenants_app/search_order_results.html'
    if 'q' in request.GET:
        q = request.GET.get('q')
        if not q:
            error = True
        else:
            orders_q = Orders.objects.filter(Q(name_item__icontains=q))
            shelfs = Shelf.objects.filter(Q(name__icontains=q))

            pagin = PaginatorMixin(request, model=shelfs, elements_on_page=10)

            context = {
                'orders_q': orders_q,
                'query': q,
                'page_object': pagin.page,
                'is_paginated': pagin.is_paginated,
                'next_url': pagin.next_url,
                'prev_url': pagin.prev_url
            }

            return render_to_response(template, context)

    return render(request, 'tenants_app/sales_ledger.html', {'error': error, 'orders': orders})


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
        if not shelf:
            raise Http404
        return render(request, 'tenants_app/view_shelf.html', {'shelf': shelf,
                                                               'act': act, 'orders': orders})
    return HttpResponse(status=405)


def create_cash(request, orders_id):
    if request.method == 'GET':
        return render(request, 'tenants_app/create_cash.html')

    elif request.method == 'POST':
        sell = request.POST['sell']
        discount = request.POST['discount']
        if not discount:
            discount = 0

        return redirect(reverse('tenants:create_cash_nal_beznal', kwargs={
            'orders_id': orders_id, 'sell': sell, 'discount': discount
        }))

    return HttpResponse(status=405)


def create_cash_nal_beznal(request, orders_id, sell, discount):
    instance = get_object_or_404(Orders, pk=orders_id)
    shelf = instance.act.shelf

    instance.quality = int(instance.quality) - int(sell)
    instance.all_sell = int(instance.all_sell) + int(sell)
    all_cash = int(sell) * float(instance.price)

    if request.method == 'POST':
        cash_form = CashForm(request.POST)

        if cash_form.is_valid():
            with transaction.atomic():
                cash = cash_form.save(commit=False)
                cash.all_cash = int(cash.sell) * float(instance.price)
                cash.save()
                instance.save()
                return redirect(reverse('tenants:view_shelf', kwargs={
                    'shelf_id': shelf.pk
                }))
        else:
            c = {'cash_form': CashForm(), 'instance': instance}
            return render(request, 'tenants_app/create_cash_nal_beznal.html', c)
    else:
        if request.method == 'GET':
            cash_form = CashForm(initial={'sell': sell, 'discount': discount, 'orders': instance})
            return render(request, 'tenants_app/create_cash_nal_beznal.html',
                          {'instance': instance, 'cash_form': cash_form,
                           'all_cash': str(all_cash)})

    return HttpResponse(status=405)


def view_cash(request):
    if request.method == 'GET':
        today = datetime.now().replace(tzinfo=pytz.UTC).date()
        cashes = Cash.objects.filter(cash_date__year=today.year,
                                     cash_date__month=today.month,
                                     cash_date__day=today.day).order_by('cash_date').reverse()

        pagin = PaginatorMixin(request, model=cashes, elements_on_page=10)

        context = {
            'today': today,
            'page_object': pagin.page,
            'is_paginated': pagin.is_paginated,
            'next_url': pagin.next_url,
            'prev_url': pagin.prev_url
        }

        return render(request, 'tenants_app/view_cash.html', context)
    return HttpResponse(status=405)


@login_required
def search_cash(request, pk):
    q = None
    today = None
    show_date = None
    cashes = None
    nal_true = request.GET.get('nal')
    nal_false = request.GET.get('notnal')
    sum_all_cash = 0
    nal_cash = 0
    not_nal_cash = 0
    template = 'tenants_app/view_cash.html'
    if pk == 0:
        nal_true = "on"
        nal_false = "on"
        today = datetime.now().replace(tzinfo=pytz.UTC).date()
        cashes = Cash.objects.filter(cash_date__gte=today).order_by('-cash_date')
    elif pk == 1:
        today = datetime.now().replace(tzinfo=pytz.UTC).date()
        cashes = Cash.objects.filter(cash_date__gte=today).order_by('-cash_date')
    elif pk == 2:
        now = datetime.now() - timedelta(weeks=1)
        cashes = Cash.objects.filter(cash_date__gte=now).order_by('-cash_date')
    elif pk == 3:
        now = datetime.now() - timedelta(weeks=4)
        cashes = Cash.objects.filter(cash_date__gte=now).order_by('-cash_date')
    elif pk == 4:
        now = datetime.now() - timedelta(weeks=52)
        cashes = Cash.objects.filter(cash_date__gte=now).order_by('-cash_date')

    elif pk == 5 and 'q' in request.GET:
        q = request.GET.get('q')
        if not q:
            cashes = None
        else:
            q_date = datetime.strptime(q, "%Y-%m-%d")
            cashes = Cash.objects.filter(Q(cash_date__icontains=datetime.date(q_date))).order_by('-cash_date')
            show_date = datetime.strftime(q_date, "%d-%m-%Y")

    if cashes:
        nal_true = request.GET.get('nal')
        if not nal_true:
            cashes = cashes.exclude(nal=True)
        nal_false = request.GET.get('notnal')
        if not nal_false:
            cashes = cashes.exclude(nal=False)

        for cash in cashes:
            sum_all_cash += cash.all_cash
            sum_all_cash = float("{0:.2f}".format(sum_all_cash))
            if cash.nal:
                nal_cash += cash.all_cash
                nal_cash = float("{0:.2f}".format(nal_cash))
            else:
                not_nal_cash += cash.all_cash
                not_nal_cash = float("{0:.2f}".format(not_nal_cash))
    else:
        cashes = None

    if not request.user.is_staff:
        if cashes:
            # фильтр продаж по авторизованному пользователю
            tenant = Tenant.objects.filter(username=request.user.username)
            cashes_tenant = Cash.objects.filter(orders__act__rents__tenants__in=tenant)
            cashes = cashes.filter(id_cash__in=cashes_tenant)

    print(nal_true)
    print(nal_false)
    if not cashes:
        cashes = []
        pagin = PaginatorMixin(request, model=cashes, elements_on_page=10)
    else:
        pagin = PaginatorMixin(request, model=cashes, elements_on_page=10)

    context = {
        'today': today,
        'cashes': cashes,
        'query': q,
        'show_date': show_date,
        'page_object': pagin.page,
        'is_paginated': pagin.is_paginated,
        'next_url': pagin.next_url,
        'prev_url': pagin.prev_url,
        'sum_all_cash': sum_all_cash,
        'nal_cash': nal_cash,
        'not_nal_cash': not_nal_cash,
        'nal': nal_true,
        'notnal': nal_false
    }

    return render(request, template, context)


def payment_to_tenant(request, username):
    tenant = Tenant.objects.filter(username=username)
    all_cashes = {}
    all_tenant_take = 0
    # расчет суммы по каждому акту
    all_acts = Act.objects.filter(rents__tenants__in=tenant)
    for act in all_acts:
        cashes = Cash.objects.filter(orders__act=act)
        sum_all_cash = 0
        values = []
        for cash in cashes:
            sum_all_cash += cash.all_cash
        values.append(sum_all_cash)

        # сколько забирает арендатель
        percent = sum_all_cash * act.category.percent_from_sales / 100
        values.append(percent)
        tenant_take = sum_all_cash - percent
        if act.category.rent_of_shelf == 'да':
            tenant_take -= act.shelf.price
        all_tenant_take += tenant_take
        values.append(tenant_take)
        all_cashes[act] = values

    # сколько нала в кассе


    context = {
        'tenant': tenant,
        'all_cashes': all_cashes,
        'all_tenant_take': all_tenant_take,
    }

    return render(request, 'tenants_app/payment_to_tenant.html', context)


def delete_cash(request, id_cash):
    instance = get_object_or_404(Cash, pk=id_cash)
    if request.method == 'GET':
        instance.delete()
        return redirect(reverse('tenants:view_cash'))
    return HttpResponse(status=405)



# not in use:

# def edit_cash(request, id_cash):
#     instance = get_object_or_404(Cash, pk=id_cash)
#     order = instance.orders
#     act = order.act
#     shelf = act.shelf
#
#     if request.method == "POST":
#         cash_form = CashForm(request.POST, instance=instance)
#
#         if cash_form.is_valid():
#             cash = cash_form.save(commit=False)
#             cash.instance = instance
#             cash.save()
#             order.quality = int(order.quality) - int(cash.sell)
#             order.all_sell = int(order.all_sell) + int(cash.sell)
#             order.save()
#
#             return redirect(reverse('tenants:view_shelf', kwargs={
#                 'shelf_id': shelf.pk
#             }))
#         else:
#             c = {'cash_form': CashForm(instance=instance), 'instance': instance}
#             return render(request, 'tenants_app/edit_cash.html', c)
#     else:
#         if request.method == 'GET':
#             return render(request, 'tenants_app/edit_cash.html',
#                           {'instance': instance, 'cash_form': CashForm(instance=instance)})
#
#     return HttpResponse(status=405)