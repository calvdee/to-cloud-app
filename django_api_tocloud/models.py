from django.db import models
from django.contrib.auth.models import User
from django_tocloud import states

# Create your models here.
class UrlUpload(models.Model):
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
