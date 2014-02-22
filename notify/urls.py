from django.conf.urls import patterns, url

from notify.views import IndexView, UpdateView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^update/$', UpdateView.as_view(), name='update'),
)
