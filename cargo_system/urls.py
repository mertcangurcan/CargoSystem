from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', include('home.urls')),
    url(r'^home/', include('home.urls')),
    url(r'^users/',include('users.urls')),
    url(r'^shipments/',include('cargo_app.urls')),
    url(r'^adminpanel/',include('useradmin.urls')),

]
