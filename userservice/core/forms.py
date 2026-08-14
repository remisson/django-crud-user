from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db.models import Q

class UserLoginForm(forms.Form):
	email = forms.EmailField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self):
		cleaned_data = super().clean()

		email = cleaned_data.get("email")
		password = cleaned_data.get("password")

		if not email:
			raise ValidationError("The email is required")

		elif not password:
			raise ValidationError("The password is required")

		elif not '@' in email or (len(email) < 4 or len(email) > 320):
			raise ValidationError("The email is invalid")

		elif len(password) < 6 or len(password) > 20:
			raise ValidationError("The password is invalid")

		elif not User.objects.filter(email__exact=email).exists():
			raise ValidationError("User not found")

		return cleaned_data

class UserCreateForm(forms.Form):
	username = forms.CharField(max_length=50, validators=[RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')])
	email = forms.EmailField()
	password = forms.CharField(widget=forms.PasswordInput)
	retry_password = forms.CharField(widget=forms.PasswordInput)

	def clean(self):
		cleaned_data = super().clean()

		username = cleaned_data.get("username")
		email = cleaned_data.get("email")
		password = cleaned_data.get("password")
		retry_password = cleaned_data.get("retry_password")

		if not username:
			raise ValidationError("The username is required")

		elif len(username) > 50:
			raise ValidationError("The username must be up to 50 characters long")

		elif not email:
			raise ValidationError("The email is required")

		elif not password:
			raise ValidationError("The password is required")

		elif not retry_password:
			raise ValidationError("The retry_password is required")

		elif password != retry_password:
			raise ValidationError("The password confirmation failed")

		elif not '@' in email or (len(email) < 4 or len(email) > 320):
			raise ValidationError("The email is invalid")

		elif len(password) < 6 or len(password) > 20:
			raise ValidationError("The password is invalid")

		elif User.objects.filter(Q(username__exact=username) | Q(email__exact=email)).exists():
			raise ValidationError("The user already exists")

		return cleaned_data
