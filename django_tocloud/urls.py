from django.conf.urls import patterns, include, url
from django_tocloud import views

urlpatterns = patterns('',
    url(r'^$', views.URLUploadFormView.as_view(), name="url_upload_view"),
    url(r'auth/$', 
    		views.DropboxAuthView.as_view(), 
    		name="dropbox_auth_view"),
)
