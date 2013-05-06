from django.conf.urls import patterns, include, url
from django_api_tocloud import views

urlpatterns = patterns('',
		(r'^upload/$', views.UrlUploadListView.as_view()),
    (r'^upload/(?P<pk>[0-9]+)$', views.UrlUploadRetrieveView.as_view()),
)

urlpatterns += patterns('',
		(r'^user/$', views.UserListView.as_view()),
    (r'^user/(?P<pk>[0-9]+)$', views.UserRetrieveView.as_view()),
)