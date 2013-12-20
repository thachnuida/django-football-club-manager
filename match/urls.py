from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from match import views
admin.autodiscover()

urlpatterns = patterns('',
  url(r'^$', views.index, name='index'),
  url(r'^add/$', views.add, name='add'),
  url(r'^edit/(?P<match_id>\d+)/$', views.edit, name='edit'),
  url(r'^detail/(?P<match_id>\d+)/$', views.detail, name='detail'),
	url(r'^delete/(?P<match_id>\d+)/$', views.delete, name='delete'),
	url(r'^add_player/(?P<match_id>\d+)/$', views.add_player, name='add_player'),
	url(r'^remove_player/(?P<match_id>\d+)/$', views.remove_player, name='remove_player'),
  url(r'^calendar/$', views.calendar, name='calendar'),
  url(r'^get_match/$', views.get_match, name='get_match'),
)
