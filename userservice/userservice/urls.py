# -*- coding: utf-8 -*-
from django.contrib import admin
from django.urls import include, path
######################################################################################
# @author Remisson dos Santos Silva
# @since 14/08/2026
######################################################################################
urlpatterns = [
    path("", include("core.urls")),
    path('admin/', admin.site.urls),
]
