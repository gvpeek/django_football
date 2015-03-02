import json
import logging
import time

from math import floor, ceil, pow
from random import randint, choice, shuffle
from copy import deepcopy
from collections import OrderedDict, deque

from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from .models import Player
from core.models import Year
from stats.models import TeamStats
from teams.models import Team, Roster

import names

# TODO see if processing speed increases by converting stub to dictionary, removing need for string & int translations
def create_player_stub(number):
    ''' player attributes are concatenated into a string which is used to track each player stub
        The attrs are packed as follows: age, rating, apex age, rating increment, rating decrement, 
        status, position
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

def get_min_max_ratings():
    return [(14,(20,50)), # (age, (min,max))
            (18,(30,60)),
            (22,(45,75)),
            (99,(60,90))]

def age_player_stub(player_data, years=1):
    ''' function to break apart player stub and age them a single year
    '''
    min_max_ratings = get_min_max_ratings()
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
        will not be referenced, a stub of necessary attributes is used in this process. The player stubs are "aged" 
        for a number of years, with the remaining unretired players being instantiated into full player records and 
        stored in the database.
    '''

    # Main Logic
    logger = logging.getLogger('django.request')
    
    pl=[]
    for x in xrange(40):
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
    
    logger.info('{0} players created in universe {1}.'.format(len(players), universe.name))

def create_players(universe, number):
    ''' This fuction is used to create players once a universe has already been initially seeded.
    '''
    logger = logging.getLogger('django.request')

    players = [Player(universe=universe,
                      first_name=names.first_name(),
                      last_name=names.last_name(),
                      age = 11,
                      position = choice(['QB','RB','WR','OT','OG','C','DT','DE','LB','CB','S','K','P']),
                      constitution = randint(25,40),
                      retired = False,
                      apex_age = (floor(((32 * 100) * pow(randint(5,100),-.5)) / 100) + 18),
                      growth_rate = randint(1,4),
                      declination_rate = randint(3,5),
                      ratings = randint(25,40)) for x in xrange(int(number))]

    Player.objects.bulk_create(players)
    
    logger.info('{0} players created in universe {1}.'.format(len(players), universe.name))

def determine_draft_needs(preference, roster):
    ''' Prioritizes positions to be drafted based on current roster. Vacant spots are put first then 
        occupied positions. Position preference is maintained within each of these.
    '''
    filled=[]
    for position in preference:
            if getattr(roster, position.lower()):
                    filled.append(position)
    shuffle(filled)
    for position in filled:
            preference.remove(position)
            preference.append(position)
            
    return preference
    
def draft_players(universe):
    logger = logging.getLogger('django.request')
    
    current_year = Year.objects.get(universe=universe,
                                    current_year=True)
    previous_year=None
    try:
        previous_year = Year.objects.get(universe=universe,
                                         year=(current_year.year - 1))
    except ObjectDoesNotExist, e:
        logger.info('No previous year - {0}'.format(e))

    teams=[]
    try:
        team_order=TeamStats.objects.filter(universe=universe,
                                          year=previous_year).order_by('pct', 'diff', 'score')
        for team_stat in team_order:
            teams.append(team_stat.team)
    except ObjectDoesNotExist, e:
        logger.info('No previous team stats - {0}'.format(e))

    if not teams:
        teams = Team.objects.filter(universe=universe)
        shuffle(list(teams))
        
    draft_preference = OrderedDict()
    nbr_positions = 0 
    for team in teams:
        try:
            roster = Roster.objects.get(universe=universe,
                                   year=current_year,
                                   team=team)
        except ObjectDoesNotExist, e:
            roster = Roster(universe=universe,
                       year=current_year,
                       team=team)
            roster.save()
            
        draft_preference[team] = deque()
        draft_preference[team].extend(determine_draft_needs(deepcopy(json.loads(team.draft_position_order)), roster))
        if nbr_positions < len(draft_preference[team]):
                nbr_positions=len(draft_preference[team])
                
    logger.info('Draft order ' + str(draft_preference))
    
    ## need to set team here for first check of presence of key
    team = draft_preference.keys()[0]
    while draft_preference:
        if not draft_preference[team]:
            del draft_preference[team]
        for team in draft_preference:
            selected = False
            while not selected and draft_preference[team]:
                pick_position = draft_preference[team].popleft()
                players = Player.objects.filter(universe=universe,
                                                position=pick_position,
                                                retired=False,
                                                signed=False,
                                                age__gte=23).order_by('ratings').reverse()
                roster = Roster.objects.get(universe=universe,
                                            year=current_year,
                                            team=team)
                player = players[0]
                current_player = getattr(roster, pick_position.lower())
                if not current_player or \
                        (player.ratings >  current_player.ratings): # and player.age < current_player.age 
                    # current_player = Player.objects.get(id=roster.pick_position.lower().id)
                    if current_player:
                        current_player.signed=False
                        current_player.save()
                        logger.info('{0} {1} {2} {3} {4} was cut.'.format(team.city,
                                                                          team.nickname,
                                                                          pick_position,
                                                                          current_player.first_name,
                                                                          current_player.last_name))
                    setattr(roster,pick_position.lower(),player)
                    setattr(roster,pick_position.lower()+'_age',player.age)
                    setattr(roster,pick_position.lower()+'_rating',player.ratings)
                    roster.save()
                    player.signed=True
                    player.save()
                    selected = True
            
                    method = 'drafted' if player.age == 23 else 'signed'
                    logger.info('{0} {1} {2} {3} {4} was {5}.'.format(team.city,
                                                                      team.nickname,
                                                                      pick_position,
                                                                      player.first_name,
                                                                      player.last_name,
                                                                      method))

def _check_rating_range(player,range):
    ''' function to check if player is within the rating range for their given age range. If a player
        is below the minimum range, they retire. If a player is above the maximum range, their rating
        is set to the maximum.
    '''
    if player.ratings < min(range):
        player.retired = True
        player.signed = False
    elif player.ratings > max(range):
        player.ratings = max(range)

@transaction.commit_manually
def age_players(universe):
    logger = logging.getLogger('django.request')
    
    min_max_ratings = get_min_max_ratings()
    active_players = list(Player.objects.filter(retired=False,universe=universe))

    players_retired = 0
    for player in active_players:
        start_time = time.time()
        player.age += 1
        if player.age <= player.apex_age:
            player.ratings += randint(1,player.growth_rate)
        else:
            player.ratings -= randint(3,player.declination_rate)
        for age,ratings in min_max_ratings:
            if player.age <= age:
                _check_rating_range(player, ratings)
                break
        if player.retired:
            players_retired += 1
        player.save()
        elapsed_time = time.time() - start_time
        logger.info("Player aged in {0} seconds".format(elapsed_time))

    start_time = time.time()        
    transaction.commit()
    elapsed_time = time.time() - start_time
    logger.info("Player aging committed in {0} seconds".format(elapsed_time))
    
    logger.info('{0} players processed. {1} players retired'.format(len(active_players), players_retired))