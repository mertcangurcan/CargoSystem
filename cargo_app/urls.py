from django.conf.urls import include, url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new/?$', views.addshipment, name='addshipment'),
    url(r'^(?P<pk>\d+)/?$', views.details, name='details'),
    url(r'^update/(?P<pk>[0-9]+)/?$', views.update, name='update'),
    url(r'^delete/(?P<pk>[0-9]+)/?$', views.delete, name='delete'),
    url(r'^gettrack/?$', views.gettrack, name='gettrack'),
    url(r'^getcorporatetrack/?$', views.getcorporatetrack, name='getcorporatetrack'),
    url(r'^user/(?P<pk>[0-9]+)/?$', views.listUserShipments, name='listUserShipments'),
    url(r'^categories/$', views.sendCategories, name='sendCategories'),
    url(r'^shiporder/$', views.shipOrder, name='shipOrder'),
   
]

