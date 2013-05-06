from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    (r'^$', TemplateView.as_view(template_name="home.html")),
    (r'^app/$', TemplateView.as_view(template_name="index.html")),
)
