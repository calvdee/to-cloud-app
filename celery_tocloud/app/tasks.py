import os
import eventlet
import requests
import statsd

from celery import group, chain, chord, Task
from dropbox import client, rest, session
from celery_tocloud.app.main import celery
from celery_tocloud.app import celeryconfig

conf = celery.conf
statsd = statsd.StatsClient(prefix='xx.apps.upload_worker')

## Helpers

def marker(length=35): print '*'*length

def get_dropbox_client(access_key, secret):
	
	# Create the session
	s = session.DropboxSession(
		conf.APP_KEY, conf.APP_SECRET, conf.ACCESS_TYPE)

	# Set the auth
	s.set_token(access_key, secret)

	# Return the client
	return client.DropboxClient(s)

## Tasks

@celery.task
def upload_file(url, access_key, secret):
	"""
	Uploads to Dropbox what `url` points to.
	"""

	marker()
	print "Received task <upload_file> for '%s'" % url

	# Obtain a client
	client = get_dropbox_client(access_key, secret)
	
	# Create the file object using requests
	url_file = requests.get(url, stream=True).raw
	url_file_name = url.split('/')[-1:][0]
	
	try:
		# Download a file and if it fails we can re-try the task
		# at whatever the last position is in the error response.
		with statsd.timer('timers.chunked_uploader'):
			uploader = client.ChunkedUploader(client, url_file)

		# Upload
		print "Beginning upload for '%s'" % url
		uploader.upload_chunked(conf.CHUNK_SIZE)

		# Commit 
		print "Committing upload for %s" % url
		uploader.finish('%s' % url_file_name, True)

	except rest.ErrorResponse as e:
		# TODO: Retry the task
		print "Failed to download file %s (%s)" % (url, str(e))


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