from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
  url(r'^$', 'drive.views.home', name = "home"),
  url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'login.html'}, name='login'),
  url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
  url(r'^register$', 'drive.views.register', name='register'),
  url(r'^verify/(?P<token>\w*)', 'drive.views.verify', name = 'verify'),
  url(r'^addAccounts$', 'drive.views.addAccounts', name='addAccounts' ),

  url(r'^addDropbox$', 'drive.views.addDropbox', name="addDropbox"),
  url(r'^dropboxCallback/$', 'drive.views.dropboxCallback', name="dropboxCallback"),

  url(r'^addGoogleDrive$', 'drive.views.addGoogleDrive', name="addGoogleDrive"),
  url(r'^googleCallback/$', 'drive.views.googleCallback', name="googleCallback"),
  
  url(r'^rename/(?P<old_account_name>\w+)/(?P<account_type>\w+)$', 'drive.views.rename', name = "rename"),



)