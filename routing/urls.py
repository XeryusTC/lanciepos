from django.conf.urls import patterns, url

from routing import views

urlpatterns = patterns('',
	url(r'^$', views.RequestAccessView.as_view(), name='request_access'),
	url(r'^success/$', views.RequestSuccessView.as_view(), name='request_success'),
	url(r'^overview/$', views.GrantAccessOverviewView.as_view(), name='grant_access_overview'),
	url(r'^overview/([\w]+)/$', views.GrantAccessOverviewView.as_view(), name='grant_access_overview_error'),
	url(r'^grant_access/(?P<client_id>\d+)/$', views.grant_access, name='grant_access'),
)

