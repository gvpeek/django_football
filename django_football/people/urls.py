from django.conf.urls import patterns, url

import people.views

urlpatterns = patterns('',
    url(r'player/history/(?P<player_id>\d+)/$', people.views.show_player_history, name='show_player_history'),
)