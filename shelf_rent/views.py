from dal import autocomplete
from tenants_app.models import *


class ShelfAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        shelfs_in_use = Act.objects.filter().values('shelf').filter(shelf__isnull=False)
        shelfs = Shelf.objects.exclude(shelf_id__in=shelfs_in_use).order_by('name')
        qs = shelfs

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
