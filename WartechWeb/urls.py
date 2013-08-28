from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
import main.views
import configurator.views
import arena.views


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', main.views.home),    
    url(r'^[Cc]onfigurator$', configurator.views.default),    
    url(r'^[Aa]rena$', arena.views.default),    
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
    )
