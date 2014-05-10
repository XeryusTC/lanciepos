from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from routing.views import RequestAccessView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lansite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

	# default stuff
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    
    # lansite stuff
    url(r'^notify/', include('notify.urls', namespace="notify")),
    url(r'^notification/', include('notify.urls')),
    url(r'^routing/', include('routing.urls', namespace="routing")),
    url(r'^bar/', include('pointofsale.urls', namespace="pos")),
    url(r'^$', RequestAccessView.as_view(), name='index'),
    url(r'js/([\w\.\-]+)/([\w\.\-]+).js$', 'lansite.views.javascript', name='javascript'),
)
