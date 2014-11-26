from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

import core.views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', core.views.index, name='index'),
    url(r'universe/create/$', core.views.universe_create, name='universe_create'),

    # Examples:
    # url(r'^$', 'django_football.views.home', name='home'),
    # url(r'^django_football/', include('django_football.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

# Uncomment the next line to serve media files in dev.
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
                            )
