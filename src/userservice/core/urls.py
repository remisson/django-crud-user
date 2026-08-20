# -*- coding: utf-8 -*-
from django.urls import path

from . import views
######################################################################################
# @author Remisson dos Santos Silva
# @since 14/08/2026
######################################################################################

urlpatterns = [
	path("", views.index, name="index"),
	path("home/", views.home, name="home"),
	path("login/", views.login, name="login"),
	path("logout/", views.logout, name="logout"),
	path("create_account/", views.create_account, name="create_account"),
	path("edit_account/<int:pk>/", views.edit_account, name="edit_account"),
	path("delete_account/<int:pk>/", views.delete_account, name="delete_account"),
]
