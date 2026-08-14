from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class CreateAccountViewTest(TestCase):

	def setUp(self):
		self.url = reverse('create_account') 

    def test_create_user_success(self):
		data = {
			'username': 'foouser',
			'email': 'foo@email.com',
			'password': 'SecurityMyAccount423',
			'retry_password': 'SecurityMyAccount423',
		}
		client_response = self.client.post(self.url, data)

		self.assertEqual(User.objects.count(), 1)

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
