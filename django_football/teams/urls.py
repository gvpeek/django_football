from django.conf.urls import patterns, url

import teams.views

urlpatterns = patterns('',
    url(r'detail/(?P<team_id>\d+)/(?P<year>\d+)/$', teams.views.show_team_detail, name='show_team_detail'),
    url(r'history/(?P<team_id>\d+)/$', teams.views.show_team_history, name='show_team_history'),
)