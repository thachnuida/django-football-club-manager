from django.conf.urls import patterns, url
from account import views

urlpatterns = patterns('',
  url(r'^$', views.index),
  url(r'^profile/$', views.profile, name='profile'),
	url(r'^list_player/(?P<user_id>.+)/$', views.edit, name='edit'),
	url(r'^delete/(?P<user_id>.+)/$', views.delete, name='delete'),
	url(r'^login/$', views.site_login, name='login'),
	url(r'^logout/$', views.site_logout, name='logout'),
	url(r'^register/$', views.register, name='register'),
	url(r'^list_player/$', views.list_player, name='list_player'),
)
