from __future__ import absolute_import

from random import randint

from celery import shared_task

from .models import Player

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