from django.contrib import admin
from match.models import Club, Match

admin.autodiscover()
admin.site.register(Club)
admin.site.register(Match)