import logging

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as django_login, logout as django_logout

from .forms import UserLoginForm, UserCreateForm

def index(request):
	return HttpResponse(loader.get_template("core/login.html").render({}, request))

@login_required
def home(request):
	return HttpResponse(loader.get_template("core/home.html").render({}, request))

def login(request):
	if request.method == 'POST':

		form = UserLoginForm(request.POST)

		if form.is_valid():
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']

			user_obj = User.objects.only('username').filter(email__exact = email).first()
			username = user_obj.username

			user = authenticate(request, username=username, password=password)

			if user is not None:
				django_login(request, user)
				logging.info('[login] SUCCESS: {}'.format(user.username))
				return redirect('home')

			else:
				messages.add_message(request, messages.ERROR, 'Invalid login')

	else:
		form = UserLoginForm()

	return render(request, 'core/login.html', {'form': form})

def logout(request):
	try:
		django_logout(request)
		request.session.flush()
		return redirect('index')
	except Exception as e:
		logging.exception('[login] ERROR: {}'.format(e))
		messages.add_message(request, messages.ERROR, '[ERROR] An internal error has occurred')
	return index(request=request)

def create_account(request):
	if request.method == 'POST':

		form = UserCreateForm(request.POST)

		if form.is_valid():
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			retry_password = form.cleaned_data['retry_password']

			user = User.objects.create_user(
				username = username,
				email = email,
				password = password,
				first_name = username,
				last_name = '',
				is_staff = False,
				is_active = True,
				is_superuser = False,
			)

			logging.info('[create_account] SUCCESS: {}'.format(user.username))
			return redirect('login')
	else:
		form = UserCreateForm()

	return render(request, 'core/create_account.html', {'form': form})
