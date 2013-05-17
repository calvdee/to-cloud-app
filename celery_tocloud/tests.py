import unittest
import requests
import json
import time

from celery_tocloud.models import OAuthToken, URLUpload
from celery_tocloud.app.tasks import upload_url, get_dropbox_client

from dropbox import rest, client

ACCESS_KEY = 'n63mv83arjv1ane'
SECRET = '4rbk8o1mu1z3tz5'

_token = OAuthToken.objects.create(access_key=ACCESS_KEY, secret=SECRET)

class DropboxTest(unittest.TestCase):
	chunk_size = 4194304

	def setUp(self):
		self.client = get_dropbox_client(_token)
		self.file_name = 'cc.txt'
		self.url_file = 'https://www.dropbox.com/static/developers/dropbox-python-sdk-1.5.1.zip'
		self.url_file_name = self.url_file.split('/')[-1:][0]

	# def tearDown(self):
	# 	self.client.file_delete('%s' % self.file_name)
	# 	self.client.file_delete('%s' % self.url_file_name)

	def test_upload_chunked_file(self):
		""" Use the ChunkedUploader to upload a file. """

		# Open the file and upload
		file_name = self.file_name

		with open(file_name, 'r') as f:
			uploader = self.client.ChunkedUploader(self.client, f)
			uploader.upload_chunked(self.chunk_size)

		# Commit the file
		uploader.finish('%s' % file_name, True)

		# Did the file get created?
		meta = self.client.search('.', file_name)
		self.assertNotEqual(len(meta), 0)


	def test_upload_chunked_url(self):
		""" Use the ChunkedUploader to upload a URL. """

		file_name = self.url_file_name

		r = requests.get(self.url_file, stream=True)

		uploader = self.client.ChunkedUploader(self.client, r.raw)
		uploader.upload_chunked(self.chunk_size)
		uploader.finish('%s' % file_name, True)

		# Did the file get created?
		meta = self.client.search('.', file_name)
		self.assertNotEqual(len(meta), 0)

	def test_fail_dropbox_client(self):
		"""
		Create a client with bad auth and c.account_info should throw
		an `ErrorResponse`.
		"""
		c = get_dropbox_client(None)
		fn = c.account_info
		
		self.assertRaises(AttributeError, fn)
		
class TasksTest(unittest.TestCase):
	url_file = 'http://dl.soundowl.com/5bez.mp3'
	file_created = False

	def setUp(self):
		self.client = get_dropbox_client(_token)
		self.url_file_name = self.url_file.split('/')[-1:][0]

	def tearDown(self):
		""" Remove the file from Dropbox if it was created. """
		if self.file_created is True:
			self.client.file_delete('%s' % self.url_file_name)

	def test_upload_url(self):
		""" Uploads the file file to Dropbox """
		
		# Setup the URLUpload properties
		email = 'calvindlm@gmail.com'
		url = self.url_file
		token = OAuthToken.objects.create(access_key=ACCESS_KEY, secret=SECRET)
		
		# Create the object
		o = URLUpload.objects.create(email=email,
																 url=url,
																 access_token=token)

		# Sanity check
		self.assertNotEqual(o.id, None)

		# Test the task method, pass in the object since celery
		# won't use the test database so it won't find the ``id``.
		upload_url(o.id, url_upload_o=o)

		# Did the file get created?
		meta = self.client.search('.', self.url_file_name)
		self.assertNotEqual(len(meta), 0)

	def test_run_url_upload(self):
		""" 
		Runs the download task calling the ``upload_file.delay`` method 
		"""
		try:
			self.client.file_delete('%s' % self.url_file_name)
		except rest.ErrorResponse:
			pass

		# Create the ``URLUpload`` object
		token = OAuthToken.objects.create(access_key=ACCESS_KEY, secret=SECRET)
		# Create the object
		o = URLUpload.objects.create(email='calvindlm@gmail.com',
																 url='http://www.greenteapress.com/thinkstats/thinkstats.pdf',
																 access_token=token)
		
		self.assertNotEqual(o.id, None)
		self.assertNotEqual(len(URLUpload.objects.filter(id=o.id)), 0)
		task = upload_url.delay(o.id, o)

		while not task.ready():
			time.sleep(1)
			print "Waiting..."
		
		# Did the file get created?
		# meta = self.client.search('.', self.url_file_name)
		# self.assertNotEqual(len(meta), 0)

		# Set for cleanup
		# self.file_created = True
		
if __name__ == '__main__':
	unittest.main()