from django.conf.urls import patterns, url

import core.views

urlpatterns = patterns('',
    url(r'create/$', core.views.universe_create, name='universe_create'),
    url(r'detail/(?P<universe_id>\d+)/$', core.views.show_leagues, name='show_leagues'),
    url(r'advance_year/(?P<universe_id>\d+)/$', core.views.advance_year, name='advance_league_year'),
)