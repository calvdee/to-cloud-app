import os
import eventlet
import requests
import statsd
import re

from django.core.mail import send_mail
from celery import group, chain, chord, Task
from dropbox import client, rest, session
from celery_tocloud.app.main import celery
from celery_tocloud.app import celeryconfig
from celery_tocloud.models import URLUpload

conf = celery.conf
statsd = statsd.StatsClient(prefix='apps.upload_worker')

## Helpers

def marker(length=50): print '*'*length

def get_dropbox_client(token):
	"""
	Creates a Dropbox session from the credentials 
	"""
	# Create the session
	s = session.DropboxSession(
		conf.APP_KEY, conf.APP_SECRET, conf.ACCESS_TYPE)

	# Set the auth
	s.set_token(token.access_key, token.secret)

	# Return the client
	return client.DropboxClient(s) 

def on_chunk_uploaded(total, url_upload): 
	""" 
	Callback for when a chunk is uploaded. Prints the number of bytes
	uploaded and the URLUpload's ``id`` and ``url``.
	"""

	print "Uploaded chunk, %s bytes total for url %s ID %s " % 
		(total, url_upload.url, url.id)

## Tasks

@celery.task
def upload_url(url_upload_id, url_upload_o=None):
	"""

	Gets the URLUpload object for the ID puts the ``url`` to Dropbox
	"""

	marker()
	print "Received task `upload_url` for URLUpload ID '%s'" % url_upload_id

	if url_upload_o is None:
		# Use an ID to get the object
		try:
			o_lst = URLUpload.objects.select_related().get(id=url_upload_id)
		except URLUpload.DoesNotExist:
			# Does not exist exception should be thrown
			raise Exception("ERROR: No URLUpload found for %s" % url_upload_id)
	else:
		# Use the passed object for testing since data does not come from test DB
		url_upload = url_upload_o

	url = url_upload.url
	token = url_upload.access_token
	
	client = get_dropbox_client(token)
	
	# Create the file object using requests
	req = requests.get(url, stream=True)
	url_file = req.raw
	url_file_name = url.split('/')[-1:][0]

	print "CONTENT-LENGTH: %s" % req.headers['content-length']

	try:
		# Upload a file and if it fails we can re-try the task
		# at whatever the last position is in the error response.

		# Stats
		# with statsd.timer('timers.url_upload'):
		
		uploader = client.ChunkedUploader(client, url_file, 57671680)

		# Upload
		print "BEGINNING upload for '%s'" % url_upload.url
		uploader.upload_chunked(chunk_size = 1 * 1024 * 1024, cb=on_chunk_uploaded)

		# Commit 
		print "COMMITING upload for '%s'" % url
		uploader.finish('%s' % url_file_name, True)

		# Send email
		send_mail("Upload complete", 
							"Your email for %s" % url_upload.url , 
							"uploads@tocloudapp.com"
    					[url_upload.email], 
    					fail_silently=False)

		url_upload.state = 
	except rest.ErrorResponse as e:
		# TODO: Retry the task
		print "Failed to upload file %s (%s)" % (url, str(e))

	url_upload.ended = datetime.today()



# # Open the file
# with open('tests.py', 'r') as f:

# 	chunk_size = self.chunk_size
# 	raw = f.read(chunk_size)
# 	last = chunk_size

# 	# While the file has bytes, upload chunk_size and save the 
# 	# last position. Use this to resume Dropbox uploads.
# 	while raw != '':
# 		raw = f.read(chunk_size)
# 		last = f.tell()