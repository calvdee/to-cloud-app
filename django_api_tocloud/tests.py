"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client, RequestFactory

from rest_framework import status

from django_api_tocloud import serializers, states
from django_api_tocloud.models import UrlUpload
from django.contrib.auth.models import User


client = Client()
factory = RequestFactory()
file_url = 'http://vts.uni-ulm.de/docs/2012/8082/vts_8082_11772.pdf'

class IntegrationTest(TestCase):
	""" Integration tests """

	def test_object_serializer(self):
		""" 
		The serializer should return is_valid() == True.
		"""
		user = User.objects.create(username='cdl',
															 password='qweqwe',
															 email='calvindlm@gmail.com')
		url = UrlUpload.objects.create(
			user=user, url='http://vts.uni-ulm.de/docs/2012/8082/vts_8082_11772.pdf')

		serialized = serializers.UrlUploadSerializer(url)

		self.assertTrue(
			[attr in serialized.data.keys() for attr in ('user', 'url',)]
		)


class UrlUploadViewTest(TestCase):
	""" 
	Tests the UrlUploadView view which supports all CRUD operations.
	"""

	def setUp(self):
		self.user = User.objects.create(username='cdl', 
																		password='qweqwe', 
																		email='calvindlm@gmail.com')

	def test_create(self):
		""" 
		POST to endpoint and an object should be created.
		"""
		endpoint = '/api/upload/'
		o = UrlUpload.objects.create(user=self.user, url=file_url)
		s_o = serializers.UrlUploadSerializer(o)

		response = client.post(endpoint, s_o.data)

		# Received 201 Created status
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

		# Can desrialize the UrlUpload object
		o_from_data = serializers.UrlUploadSerializer(data=response.data)
		self.assertTrue(o_from_data.is_valid())



class UrlUploadTest(TestCase):
	""" Tests the UrlUpload model """

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

		# UrlUpload
		url = "http://vts.uni-ulm.de/docs/2012/8082/vts_8082_11772.pdf"
		upload = UrlUpload.objects.create(user=user, url=url)

		self.assertEqual(upload.state, states.CREATED)