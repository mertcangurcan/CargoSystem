from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^register/?$', views.register, name='register'),
    url(r'^login/?$', views.login, name='login'),
    url(r'^logout/?$', views.logout, name='logout'),
    url(r'^update/(?P<pk>[0-9]+)/?$', views.update, name='update'),
    url(r'^edituser/(?P<pk>[0-9]+)/?$', views.edituser, name='edituser'),
    url(r'^delete/(?P<pk>[0-9]+)/?$', views.delete, name='delete'),
    url(r'^makeadmin/(?P<pk>[0-9]+)/?$', views.makeadmin, name='makeadmin'),
    url(r'^profile/(?P<pk>[0-9]+)/?$', views.details, name='details'),
    url(r'^adduser/?$', views.adduser, name='adduser'),
    
   
]