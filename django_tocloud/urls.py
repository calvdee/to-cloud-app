from django.conf.urls import patterns, include, url
from django_tocloud import views

urlpatterns = patterns('',
    url(r'^$', views.URLUploadFormView.as_view(), name="upload_url_view"),
    url(r'auth/$', views.DropboxAuthView.as_view(), name="dropbox_auth_view"),
    url(r'final/$', views.FinalView.as_view(), name="final_view"),
)
