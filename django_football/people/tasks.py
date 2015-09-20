from __future__ import absolute_import

import logging

from random import randint

from celery import shared_task

from .models import Player
from teams.models import Roster


LOGGER = logging.getLogger('django.request')


def determine_player_rating(age, apex_age, ratings, growth_rate, declination_rate):
    if age <= apex_age:
        ratings += randint(1,growth_rate)
    else:
        ratings -= randint(3,declination_rate)
    
    return ratings


@shared_task
def calculate_future_ratings(universe):
    active_players = Player.objects.filter(retired=False, universe=universe)
    
    for player in active_players:
        player.future_ratings = determine_player_rating(player.age,
                                                        player.apex_age,
                                                        player.ratings,
                                                        player.growth_rate,
                                                        player.declination_rate)
        player.save()


@shared_task
def sign_players(universe, current_year):
    '''
    Sweep of all players in a given universe and year to ensure those on rosters have been signed.
    :param universe:
    :param current_year:
    :return:
    '''
    rosters = Roster.objects.filter(universe=universe, year=current_year)
    for roster in rosters:
        for position in ['QB','RB','WR','OT','OG','C','DT','DE','LB','CB','S','K','P']:
            player = getattr(roster, position.lower())
            db_player = Player.objects.get(id=player.id)
            if not db_player.signed:
                LOGGER.info('{0} {1} {2} - {3} {4} ({5}) not signed!!!!'.format(position,
                                                                                roster.team.city,
                                                                                roster.team.nickname,
                                                                                db_player.first_name,
                                                                                db_player.last_name,
                                                                                db_player.ratings))
                db_player.signed = True
                db_player.save()
            if db_player.retired:
                LOGGER.info('{0} {1} {2} - {3} {4} ({5}) retired!!!!'.format(position,
                                                                             roster.team.city,
                                                                             roster.team.nickname,
                                                                             db_player.first_name,
                                                                             db_player.last_name,
                                                                             db_player.ratings))
                db_player.signed = False
                db_player.save()
