# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.exceptions import ValidationError
from .forms import UserLoginForm, UserCreateForm, UserEditForm
######################################################################################
# @author Remisson dos Santos Silva
# @since 14/08/2026
######################################################################################
User = get_user_model()
################################################################
# views
################################################################
class IndexViewTest(TestCase):

	def setUp(self):
		self.client = self.client_class()
		self.user = User.objects.create_user(
			username="tester",
			email="tester@example.com",
			password="validpass"
		)

	def tearDown(self):
		User.objects.filter(username__exact="tester").delete()

	def test_index_view(self):
		response = self.client.get(reverse("index"))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "core/login.html")

class HomeViewTest(TestCase):

	def setUp(self):
		self.client = self.client_class()
		self.user = User.objects.create_user(
			username="tester",
			email="tester@example.com",
			password="validpass"
		)

	def tearDown(self):
		User.objects.filter(username__exact="tester").delete()

	def test_home_requires_login(self):
		response = self.client.get(reverse("home"))
		self.assertRedirects(response, f"{reverse('login')}?next={reverse('home')}")
		self.client.login(username="tester", password="validpass")
		response = self.client.get(reverse("home"))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "core/home.html")

class LoginViewTest(TestCase):

	def setUp(self):
		self.client = self.client_class()
		self.user = User.objects.create_user(
			username="tester",
			email="tester@example.com",
			password="validpass"
		)

	def tearDown(self):
		User.objects.filter(username__exact="tester").delete()

	def test_login_get(self):
		response = self.client.get(reverse("login"))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "core/login.html")

	def test_login_post_success(self):
		response = self.client.post(reverse("login"), {
			"email": "tester@example.com",
			"password": "validpass"
		})
		self.assertRedirects(response, reverse("home"))

	def test_login_post_invalid(self):
		response = self.client.post(reverse("login"), {
			"email": "tester@example.com",
			"password": "wrongpass"
		})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "core/login.html")
		self.assertContains(response, "Invalid login")

class LogoutViewTest(TestCase):

	def setUp(self):
		self.client = self.client_class()
		self.user = User.objects.create_user(
			username="tester",
			email="tester@example.com",
			password="validpass"
		)

	def tearDown(self):
		User.objects.filter(username__exact="tester").delete()

	def test_logout_view(self):
		self.client.login(username="tester", password="validpass")
		response = self.client.get(reverse("logout"))
		self.assertRedirects(response, reverse("index"))

class CreateAccountViewTest(TestCase):

	def setUp(self):
		self.client = self.client_class()
		self.user = User.objects.create_user(
			username="tester",
			email="tester@example.com",
			password="validpass"
		)
		self.url = reverse('create_account') 

	def tearDown(self):
		User.objects.filter(username__exact="tester").delete()

	def test_create_account_get(self):
		response = self.client.get(reverse("create_account"))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "core/create_account.html")

	def test_create_account_post_success(self):
		response = self.client.post(reverse("create_account"), {
			"username": "newuser",
			"email": "newuser@example.com",
			"password": "validpass",
			"retry_password": "validpass"
		})
		self.assertRedirects(response, reverse("login"))
		self.assertTrue(User.objects.filter(username="newuser").exists())

	def test_create_user_success(self):
		data = {
			'username': 'foouser',
			'email': 'foo@email.com',
			'password': 'SecurityMyAccount423',
			'retry_password': 'SecurityMyAccount423',
		}
		client_response = self.client.post(self.url, data)

		self.assertEqual(User.objects.filter(username="foouser").count(), 1)

		usuario = User.objects.get(email='foo@email.com')
		self.assertNotEqual(usuario.password, 'SecurityMyAccount423')

	def test_duplicated_email_failure(self):
		User.objects.create_user(username='boo', email='boo@email.com', password='123456789')

		data = {
			'username': 'newer',
			'email': 'boo@email.com',
			'password': '456fdsfsd2332',
			'retry_password': '456fdsfsd2332',
		}
		client_response = self.client.post(self.url, data)

		self.assertEqual(User.objects.filter(username__exact='newer').count(), 0)

	def test_invalid_email_failure(self):
		User.objects.create_user(username='boo', email='boo@email.com', password='123456789')

		data = {
			'username': 'newer',
			'email': 'booemail.com',
			'password': '456fdsfsd2332',
			'retry_password': '456fdsfsd2332',
		}
		client_response = self.client.post(self.url, data)

		self.assertEqual(User.objects.filter(username__exact='newer').count(), 0)

	def test_duplicated_username_failure(self):
		User.objects.create_user(username='boo', email='boo@email.com', password='123456789')

		data = {
			'username': 'boo',
			'email': 'boo22@email.com',
			'password': '456fdsfsd2332',
			'retry_password': '456fdsfsd2332',
		}
		client_response = self.client.post(self.url, data)

		self.assertEqual(User.objects.filter(username__exact='newer').count(), 0)

class EditAccountViewTest(TestCase):

	def setUp(self):
		self.client = self.client_class()
		self.user = User.objects.create_user(
			username="tester",
			email="tester@example.com",
			password="validpass"
		)

	def tearDown(self):
		User.objects.filter(username__exact="tester").delete()

	def test_edit_account_get(self):
		self.client.login(username="tester", password="validpass")
		response = self.client.get(reverse("edit_account", args=[self.user.pk]))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "core/edit_account.html")

	def test_edit_account_post_success(self):
		self.client.login(username="tester", password="validpass")
		response = self.client.post(reverse("edit_account", args=[self.user.pk]), {
			"username": "tester_updated",
			"email": "tester@example.com"
		})
		self.assertRedirects(response, reverse("home"))
		self.user.refresh_from_db()
		self.assertEqual(self.user.username, "tester_updated")

class DeleteAccountViewTest(TestCase):

	def setUp(self):
		self.client = self.client_class()
		self.user = User.objects.create_user(
			username="tester",
			email="tester@example.com",
			password="validpass"
		)

	def tearDown(self):
		User.objects.filter(username__exact="tester").delete()

	def test_delete_account_success(self):
		self.client.login(username="tester", password="validpass")
		response = self.client.get(reverse("delete_account", args=[self.user.pk]))
		self.assertRedirects(response, reverse("index"))
		self.assertFalse(User.objects.filter(pk=self.user.pk).exists())
################################################################
# forms
################################################################
class UserLoginFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tester",
            email="tester@example.com",
            password="validpass"
        )

    def test_valid_login(self):
        form = UserLoginForm(data={
            "email": "tester@example.com",
            "password": "validpass"
        })
        self.assertTrue(form.is_valid())

    def test_missing_email(self):
        form = UserLoginForm(data={"password": "validpass"})
        self.assertFalse(form.is_valid())
        self.assertIn("The email is required", form.errors["__all__"])

    def test_invalid_email_format(self):
        form = UserLoginForm(data={"email": "invalid", "password": "validpass"})
        self.assertFalse(form.is_valid())
        self.assertIn("The email is required", form.errors["__all__"])

    def test_user_not_found(self):
        form = UserLoginForm(data={"email": "nouser@example.com", "password": "validpass"})
        self.assertFalse(form.is_valid())
        self.assertIn("User not found", form.errors["__all__"])

class UserCreateFormTests(TestCase):
	def test_valid_creation(self):
		form = UserCreateForm(data={
			"username": "newuser",
			"email": "newuser@example.com",
			"password": "validpass",
			"retry_password": "validpass"
		})
		self.assertTrue(form.is_valid())

	def test_password_mismatch(self):
		form = UserCreateForm(data={
			"username": "newuser",
			"email": "newuser@example.com",
			"password": "validpass",
			"retry_password": "wrongpass"
		})
		self.assertFalse(form.is_valid())
		self.assertIn("The password confirmation failed", form.errors["__all__"])

	def test_existing_user(self):
		User.objects.create_user(username="existing", email="existing@example.com", password="validpass")
		form = UserCreateForm(data={
			"username": "existing",
			"email": "existing@example.com",
			"password": "validpass",
			"retry_password": "validpass"
		})
		self.assertFalse(form.is_valid())
		self.assertIn("The user already exists", form.errors["__all__"])

	def test_invalid_username_characters(self):
		form = UserCreateForm(data={
			"username": "invalid_user!",
			"email": "valid@example.com",
			"password": "validpass",
			"retry_password": "validpass"
		})
		self.assertFalse(form.is_valid())
		self.assertIn("Only alphanumeric characters are allowed.", form.errors["username"])

class UserEditFormTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			username="edituser",
			email="edituser@example.com",
			password="validpass"
		)

	def test_valid_edit(self):
		form = UserEditForm(instance=self.user, data={
			"username": "edituser",
			"email": "edituser@example.com"
		})
		self.assertTrue(form.is_valid())

	def test_missing_username(self):
		form = UserEditForm(instance=self.user, data={"email": "edituser@example.com"})
		self.assertFalse(form.is_valid())
		self.assertIn("The username is required", form.errors["__all__"])

	def test_invalid_email(self):
		form = UserEditForm(instance=self.user, data={"username": "edituser", "email": "invalid"})
		self.assertFalse(form.is_valid())
		self.assertIn("The email is required", form.errors["__all__"])

	def test_user_not_found(self):
		form = UserEditForm(instance=self.user, data={"username": "nouser", "email": "nouser@example.com"})
		self.assertFalse(form.is_valid())
		self.assertIn("User not found", form.errors["__all__"])
