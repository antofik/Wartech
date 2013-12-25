from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
import main.views
import battles.views
import map.views


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', main.views.home),
    
    url(r'^is_authorized$', main.views.get_is_authorized),
    url(r'^get_all_users$', main.views.get_all_users),
    url(r'^request_fight$', main.views.request_fight),
    url(r'^get_all_modules$', main.views.get_all_modules),
    url(r'^get_user_robot$', main.views.get_user_robot),
    url(r'^get_user_modules$', main.views.get_user_modules),
    url(r'^set_module_to_slot$', main.views.set_module_to_slot),
    url(r'^map/get\?x=([0-9]+)&y=([0-9]+)$', map.views.get),
    url(r'^generate/([0-9]+)-([0-9]+)$', map.views.generate_map),
    url(r'^login$', main.views.login),
    url(r'^logout$', main.views.logout),

    url(r'^test_fight$', battles.views.test_fight),
    
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
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
