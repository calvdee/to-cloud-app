from django.db import models
from django.contrib.auth.models import User
from django_tocloud import states
from dropbox import client, rest, session

# Create your models here.
class URLUpload(models.Model):
	"""
	A URL to upload to dropbox that belongs to a User and has state.
	"""
	user = models.ForeignKey(User, null=True)
	url = models.URLField()	
	state = models.IntegerField(default=states.CREATED)


class OAuthToken(models.Model):
	"""
	An OAuth token that is saved when a user successfully authenticates with
	Dropbox.
	"""
	user = models.ForeignKey(User)
	access_key = models.CharField(max_length=50)
	secret = models.CharField(max_length=50)

class DropboxConfig():
	APP_KEY = '3wt9hriil3ozkwb'
	APP_SECRET = 'yqjvj22cenl85bv'
	ACCESS_TYPE = 'app_folder'

	@staticmethod
	def get_session():
		return session.DropboxSession(DropboxConfig.APP_KEY, 
																	DropboxConfig.APP_SECRET, 
																	DropboxConfig.ACCESS_TYPE)
