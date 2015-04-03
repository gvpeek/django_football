from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

import core.views
import leagues.views
import teams.views
import stats.views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', core.views.index, name='index'),

    url(r'^universe/', include('core.urls')),
    
    url(r'^league/', include('leagues.urls')),
    
    url(r'team/', include('teams.urls')),
    
    url(r'^stats/', include('stats.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

)

# Uncomment the next line to serve media files in dev.
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
                            )
