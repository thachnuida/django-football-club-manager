from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
  url(r'^$', 'match.views.index'),
  url(r'^account/', include('account.urls', namespace='account')),
  url(r'^accounts/', include('accounts.urls', namespace='accounts')),
  url(r'^admin/', include(admin.site.urls)),
  url(r'^match/', include('match.urls', namespace='match')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
