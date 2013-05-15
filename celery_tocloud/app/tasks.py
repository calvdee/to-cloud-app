import os
import eventlet
import requests
import statsd
import re

from celery import group, chain, chord, Task
from dropbox import client, rest, session
from celery_tocloud.app.main import celery
from celery_tocloud.app import celeryconfig
from celery_tocloud.models import URLUpload
# from BeautifulSoup import BeautifulSoup, SoupStrainer

conf = celery.conf
statsd = statsd.StatsClient(prefix='apps.upload_worker')

## Helpers

def marker(length=35): print '*'*length

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

# def log(msg):
# 	print 

## Tasks

@celery.task
def upload_url(url_upload_id):
	"""
	Gets the URLUpload object for the ID puts the ``url`` to Dropbox
	"""

	marker()
	print "Received task `upload_url` for URLUpload ID '%s'" % url_upload_id

	# Obtain a client using object from url_upload_id 
	o_lst = URLUpload.objects.select_related().filter(id=url_upload_id)

	if len(o_lst) is 0:
		# No object
		raise Exception("ERROR: No URLUpload found for %s" % url_upload_id)

	url_upload = o_lst[0]
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
		def callback(total): print "Recieved %s" % total

		print "Beginning upload for '%s'" % url_upload.url

		print "Uploading chunk"
		uploader.upload_chunked(chunk_size = 1 * 1024 * 1024)
		print "Finished uploading chunk"

		# Commit 
		print "Committing upload for '%s'" % url
		uploader.finish('%s' % url_file_name, True)

	except rest.ErrorResponse as e:
		# TODO: Retry the task
		print "Failed to upload file %s (%s)" % (url, str(e))


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