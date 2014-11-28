from math import floor, pow
from random import randint, choice

from django.shortcuts import render

from .models import Player
import names

# TODO see if processing speed increases by converting stub to dictionary, removing need for string & int translations
def create_player_stub(number):
    ''' player attributes are concatenated into a string which is used to track each player stub
    '''
    players = ['11' + str(randint(25,40)) +
               str(int((floor(((32 * 100) * pow(randint(5,100),-.5)) / 100) + 18))) +
               str(randint(1,4)) +
               str(randint(3,5)) +
               'A' +
               choice(['QB','RB','WR','OT','OG','C','DT','DE','LB','CB','S','K','P'])
                   for x in xrange(int(number))]

    return players

def _check_rating_range_stub(rating, rating_range, status):
    ''' function to check if player is within the rating range for their given age range. If a player
        is below the minimum range, they retire. If a player is above the maximum range, their rating
        is set to the maximum.
    '''
    if rating < min(rating_range):
        status = 'R'
    elif rating > max(rating_range):
        rating = max(rating_range)
    return rating, status

def age_player_stub(player_data, years=1):
    ''' function to break apart player stub and age them a single year
    '''
    min_max_ratings = [(14,(20,50)), # (age, (min,max))
                       (18,(30,60)),
                       (22,(45,75)),
                       (99,(60,90))]
    age, rating, apex, inc, dec, status, position = (int(player_data[:2]), 
                                                     int(player_data[2:4]), 
                                                     int(player_data[4:6]),
                                                     int(player_data[6]),
                                                     int(player_data[7]),
                                                     player_data[8],
                                                     player_data[9:])
    for y in xrange(int(years)):        
        age += 1
        if age <= apex:
                rating += randint(1,inc)
        else:
                rating -= randint(3,dec)
        for range_max,ratings in min_max_ratings:
                if age <= range_max:
                        rating, status = _check_rating_range_stub(rating, ratings, status)
                        break
        return str(age)+str(rating)+str(apex)+str(inc)+str(dec)+status+position

def seed_universe_players(universe, players_per_year):
    ''' This is a function to create, in bulk, the initial set of players for a given universe. Since the players 
        will not be referenced, a stub of necessary attributes is used in this process. The player stubs are "aged" for 
        50 years, with the remaining unretired players being instantiated into full player records and stored in 
        the database.
    '''

    # Main Logic
    pl=[]
    for x in xrange(50):
        pl = [age_player_stub(player) for player in pl]        
        pl = [player for player in pl if player[8] != 'R']
        pl.extend(create_player_stub(players_per_year))

    players=[]
    for p in pl:
        age, rating, apex, inc, dec, status, position = (int(p[:2]), 
                                                         int(p[2:4]), 
                                                         int(p[4:6]),
                                                         int(p[6]),
                                                         int(p[7]),
                                                         p[8],
                                                         p[9:])
        players.extend([Player(universe=universe,
                               first_name=names.first_name(),
                               last_name=names.last_name(),
                               age = age,
                               position = position,
                               constitution = randint(25,40),
                               retired = False,
                               apex_age = apex,
                               growth_rate = inc,
                               declination_rate = dec,
                               ratings = rating)])

    Player.objects.bulk_create(players)  