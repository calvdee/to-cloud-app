from django.db import models
from django_tocloud import states
from dropbox import client, rest, session
from django.core.mail import send_mail
from django.conf import settings

# Create your models here.

class OAuthToken(models.Model):
	"""
	An OAuth token that is saved when a user successfully authenticates with
	Dropbox.
	"""
	access_key = models.CharField(max_length=50)
	secret = models.CharField(max_length=50)


class URLUpload(models.Model):
	"""
	A URL to upload to dropbox that belongs to a User and has state.
	"""
	email = models.EmailField()
	url = models.URLField()	
	access_token = models.ForeignKey(OAuthToken)
	state = models.IntegerField(default=states.CREATED)
	created = models.DateTimeField(auto_now_add=True)
	started = models.DateTimeField(null=True)
	ended = models.DateTimeField(null=True)

	def send_success_email(self):
		"""
		Sends a success email to ``email`` to notify that the upload has
		completed to Dropbox.
		"""
		print "SENDING with %s" % settings.EMAIL_HOST
		print "SENDING with %s" % settings.EMAIL_PORT
		# Straight example rip, just use to console to verify.
		send_mail('Subject here', 'Here is the message.', 'from@example.com',
			['to@example.com'], fail_silently=False)

class DropboxConfig():
	app_key = settings.APP_KEY
	app_secret = settings.APP_SECRET
	access_type = settings.ACCESS_TYPE

	@staticmethod
	def get_session():
		return session.DropboxSession(DropboxConfig.APP_KEY, 
																	DropboxConfig.APP_SECRET, 
																	DropboxConfig.ACCESS_TYPE)
