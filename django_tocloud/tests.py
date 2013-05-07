from django.test.client import Client, RequestFactory
from django.test import TestCase
from django.contrib.auth.models import User

from django_tocloud import states
from django_tocloud.models import URLUpload
from django_tocloud.views import URLUploadFormView
from django.core.urlresolvers import reverse
# Your tests here

factory = RequestFactory()
client = Client()

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

class URLUploadFormViewTest(TestCase):
	""" 
	Tests the ``UrlUploadFormView`` view which sets a test cookie and renders
	the ``AuthenticationFormView``.

	The request to ``AuthenticationFormView`` should get the session from the 
	``UrlUploadFormView`` response.
	"""
	view = URLUploadFormView


	def test_set_test_cookie(self):
		data = { 'url': 'http://github.com/django/django/blob/master/django/views/generic/edit.py'}
		
		# Get the response
		response = client.post(reverse('url_upload_view'), data)

		# Make sure the test cookie was set
		self.assertFalse(client.session == {})
		self.assertNotEqual(client.session.get('testcookie'), None)
		
		

		

	



	