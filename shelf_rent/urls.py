"""shelf_rent URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from .views import ShelfAutocomplete
from shelf_rent_auth import urls as auth_urls
from tenants_app import urls as tenants_urls
from tenants_app.views import index

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),

    path('auth/', include(auth_urls, namespace='auth_app')),
    path('tenants/', include(tenants_urls, namespace='tenants')),

    path('shelf_autocomplete/', ShelfAutocomplete.as_view(), name='shelf_autocomplete'),
    path('', index, name='index'),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
