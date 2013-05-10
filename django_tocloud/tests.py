from urlparse import urlparse
from django.test.client import Client, RequestFactory
from django.test import TestCase
from django.contrib.auth.models import User

from django_tocloud import states
from django_tocloud.models import URLUpload, DropboxConfig, OAuthToken
from django_tocloud.views import URLUploadFormView, FinalView
from django.core.urlresolvers import reverse

from redis_sessions.session import SessionStore

factory = RequestFactory()

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


	def test_session(self):
		client = Client()

		data = { 
			'url': 'http://abc.com',
			'email': 'myemail@address.com'
		}
		
		# POST to get the session
		response = client.post(reverse('url_upload_view'), data)

		# Make sure the test cookie was set
		self.assertNotEqual(client.session, {})
		self.assertNotEqual(client.session.get('testcookie'), None)

		# Make sure the `dropbox_auth_url` and `url` were set
		self.assertNotEqual(client.session.get('dropbox_auth_url'), None)
		self.assertNotEqual(client.session.get('url'), None)
		

	def test_generate_drobox_auth(self):
		"""
		The ``generate_drobox_auth`` method should add the Dropbox auth URL
		and access token to the session.
		"""

		# Make sure the DropboxConfig class works
		session = DropboxConfig.get_session()
		self.assertNotEqual(session, None)

		# Call the method and make sure dropbox_auth_url and
		# request token were set
		s = SessionStore()
		view = URLUploadFormView()
		view.generate_drobox_auth(s)

		# The keys that the method should have generated exist
		self.assertTrue('dropbox_auth_url' in s.keys())
		self.assertTrue('request_token' in s.keys())

		# There is a valid dropbox URL
		parsed = urlparse(s['dropbox_auth_url'])
		self.assertEqual(parsed.netloc, 'www.dropbox.com')


class DropboxAuthViewTest(TestCase):
	"""
	Tests the ``DropboxAuthView``.  If there is no session, there should be
	some kind of exception message generated.
	"""

	def test_no_session(self):
		"""
		GETing the DropboxAuthView should redirect returning 302 status code
		when there is no session.
		"""
		client = Client()

		response = client.get(reverse('dropbox_auth_view'))

		self.assertEqual(response.status_code, 302)
		self.assertEqual(client.session, {})


class FinalViewTest(TestCase):
	"""
	Tests the FinalView which creates the URLUpload and OAuthToken objects
	when there is valid session data.
	"""

	def setUp(self):
		"""
		Create the mock session.
		"""
		s = SessionStore()
		view = URLUploadFormView()
		view.generate_drobox_auth(s)

		self.session = s

	def test_create_access_token(self):
		"""
		Method should return an OAuthToken object.
		"""
		pass