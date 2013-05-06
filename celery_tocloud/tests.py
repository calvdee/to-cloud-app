import unittest
import requests
import json
from celery_tocloud.app.tasks import upload_file, get_dropbox_client
from dropbox import rest, client

ACCESS_KEY = 'n63mv83arjv1ane'
SECRET = '4rbk8o1mu1z3tz5'

dropbox_client = get_dropbox_client(ACCESS_KEY, SECRET)

class DropboxTest(unittest.TestCase):
	chunk_size = 4194304

	def setUp(self):
		self.client = dropbox_client
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
		c = get_dropbox_client("xx", "xx")
		fn = c.account_info
		
		self.assertRaises(rest.ErrorResponse, fn)
		
class TasksTest(unittest.TestCase):
	url_file = 'https://github.com/dropbox/async_dropbox/archive/master.zip'

	def setUp(self):
		self.client = dropbox_client
		self.url_file_name = self.url_file.split('/')[-1:][0]

	def tearDown(self):
		self.client.file_delete('%s' % self.url_file_name)

	def test_upload_file(self):
		""" Uploads the file file to Dropbox """
		
		upload_file(self.url_file, ACCESS_KEY, SECRET)

		# Did the file get created?
		meta = self.client.search('.', self.url_file_name)
		self.assertNotEqual(len(meta), 0)

	def test_run_upload_file(self):
		""" 
		Runs the download task calling the ``upload_file.delay`` method 
		"""
		try:
			self.client.file_delete('%s' % self.url_file_name)
		except rest.ErrorResponse:
			pass

		t = upload_file.delay(self.url_file, ACCESS_KEY, SECRET)

		while t.state is "PENDING":
			print "Waiting for task to complete..."
		
		# Did the file get created?
		meta = self.client.search('.', self.url_file_name)
		self.assertNotEqual(len(meta), 0)

		
if __name__ == '__main__':
	unittest.main()