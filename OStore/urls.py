from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
  url(r'^drive/', include('drive.urls')),
)
