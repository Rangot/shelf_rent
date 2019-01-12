from django.core.paginator import Paginator
from django.db import models

# import os
# from io import BytesIO, StringIO
# from django.http import HttpResponse
# from django.template.loader import get_template
# from shelf_rent import settings

# from xhtml2pdf import pisa


class CustomBooleanField(models.BooleanField):

    def from_db_value(self, value, expression, connection, context):
        if value is True:
            return True
        if value is False:
            return False
        return int(value) # return 0/1


class PaginatorMixin:
    def __init__(self, request, model, elements_on_page):

        paginator = Paginator(model, elements_on_page)

        page_number = request.GET.get('page', 1)
        self.page = paginator.get_page(page_number)

        self.is_paginated = self.page.has_other_pages()

        if self.page.has_previous():
            self.prev_url = 'page={}'.format(self.page.previous_page_number())
        else:
            self.prev_url = ''

        if self.page.has_next():
            self.next_url = 'page={}'.format(self.page.next_page_number())
        else:
            self.next_url = ''

        return



'''
def fetch_pdf_resources(uri, rel):
    #if uri.find(settings.MEDIA_URL) != -1:
    #    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ''))

    if uri.find(settings.STATIC_URL) != -1:
        path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ''))
    else:
        path = None
    return path


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    #result = BytesIO()
    result = BytesIO()
    #pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result, encoding='utf-8', link_callback=fetch_pdf_resources)
    pdf = pisa.CreatePDF(BytesIO(html.encode('UTF-8')), result, encoding='UTF-8', show_error_as_pdf=True)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
'''