from django.conf.urls import patterns, url
from accounts import views

urlpatterns = patterns('',
  url(r'^login/(?P<provider>\w*)', views.login, name='login'),
)
