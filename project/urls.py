# coding: utf-8
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('a/', include('apps.alleria.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
      path(r'__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
