from django.conf.urls import patterns, url

from pointofsale import views

urlpatterns = patterns('',
    url(r'^$', views.BuyDrinkView.as_view(), name='buy_drink'),
    url(r'^buydrink/$', views.BuyDrinkView.as_view(), name='buy_action'),
    url(r'^register/$', views.RegisterParticipantView.as_view(), name='register'),
    url(r'^register_done/(?P<participant>\d+)/$', views.RegisterDoneView.as_view(), name='finish_register'),
    url(r'^moar/$', views.ToolsView.as_view(), name='tools'),
)
