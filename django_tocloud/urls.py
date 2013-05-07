from django.conf.urls import patterns, include, url
from django_tocloud.views import UrlUploadFormView

urlpatterns = patterns('',
    url(r'^$', UrlUploadFormView.as_view()),
)
