from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
 	url(r'^$', 'matchs.views.index'),
    url(r'^(?P<match_id>\d+)/$', 'matchs.views.detail'),
    url(r'^(?P<match_id>\d+)/add/$', 'matchs.views.add'),
    url(r'^(?P<match_id>\d+)/edit/$', 'matchs.views.edit'),
    url(r'^(?P<match_id>\d+)/delete/$', 'matchs.views.delete'),
)
