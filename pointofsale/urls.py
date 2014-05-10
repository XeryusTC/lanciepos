from django.conf.urls import patterns, url

from pointofsale import views

urlpatterns = patterns('',
    url(r'^$', views.BuyDrinkView.as_view(), name='buy_drink'),
    url(r'^buydrink/$', views.BuyDrinkView.as_view(), name='buy_action'),
)
