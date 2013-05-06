from django.test.client import Client, RequestFactory
from django.test import TestCase
from django.contrib.auth.models import User

from django_tocloud import states
from django_tocloud.models import URLUpload
# Your tests here

class URLUploadTest(TestCase):
	""" Tests the URLUpload model """

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_models(self):
		""" Test the model classes """

		# User
		user = User.objects.create(username="Calvin",
										 email="calvindlm@gmail.com",
										 password="qweqwe")

		query = User.objects.filter(id=user.id)

		self.assertNotEqual(user.id, None)
		self.assertNotEqual(len(query), 0)

		# URLUpload
		url = "http://vts.uni-ulm.de/docs/2012/8082/vts_8082_11772.pdf"
		upload = URLUpload.objects.create(user=user, url=url)

		self.assertEqual(upload.state, states.CREATED)

class HomeViewTest(TestCase):
	""" 
	Tests the HomeView which contains the URLUpload form.
	"""
	pass