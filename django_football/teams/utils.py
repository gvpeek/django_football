import os
import csv
import json
import pickle
import logging

from random import choice, randint, shuffle

from django.core.exceptions import ObjectDoesNotExist

import python_football

from settings.base import SITE_ROOT

from .models import Playbook, City, Nickname, Team
from people import names
from people.models import Coach, Player
from teams.models import get_draft_position_order

CSV_SOURCE_DIR = os.path.join(SITE_ROOT, 'teams', 'csv_source_files')

## Initialization Functions

def create_playbook():
    playbook = Playbook(name='Basic',
                        plays=json.dumps(pickle.dumps(python_football.new_playbook())))
    playbook.save()

def initialize_cities():
    cities = []
    with open(os.path.join(CSV_SOURCE_DIR, 'metroareas.csv'), 'r') as cities_file:
        cities_reader = csv.reader(cities_file,delimiter=',')
        for city in cities_reader:
            cities.append(City(name=city[0],
                               state = city[1],
                               pro = bool(int(city[2])),
                               semipro = bool(int(city[3])),
                               amateur = bool(int(city[4])),
                               region = city[5],
                               division = city[6],
                               )
                          )
    City.objects.bulk_create(cities)

def initialize_nicknames():
    nicknames = [] 
    with open(os.path.join(CSV_SOURCE_DIR, 'nicknames.csv'), 'r') as nicknames_file:
        nickname_reader = csv.reader(nicknames_file,delimiter=',')
        for nickname in nickname_reader:
            nicknames.append(Nickname(name=nickname[0],
                                      pro = bool(int(nickname[1])),
                                      semipro = bool(int(nickname[2]))
                                      )
                             )
    Nickname.objects.bulk_create(nicknames)   

# TODO investigate better way of testing presence of data
def initialize_team_source_data():
    try:
        Playbook.objects.get(id=1)
    except ObjectDoesNotExist:
        create_playbook()
        
    try:
        City.objects.get(id=1)
    except ObjectDoesNotExist:
        initialize_cities()
        
    try:
        Nickname.objects.get(id=1)
    except ObjectDoesNotExist:
        initialize_nicknames()

## Universe Creation Functions

def determine_number_pro_teams(universe):
    position_counts=[]
    for position in ['qb', 'rb', 'wr', 'og', 'c', 'ot', 'dt', 'de', 'lb', 'cb', 's', 'k', 'p']: 
        position_counts.append(Player.objects.filter(universe=universe, 
                                                     position=position.upper(), 
                                                     age__gte=23, 
                                                     ratings__gte=70).count())
    return sum(position_counts) / len(position_counts)

def create_initial_universe_teams(universe, level):
    logger = logging.getLogger('django.request')
    
    number_teams = determine_number_pro_teams(universe)
    cities = []
    nicknames = []
    if level == 'any':
        while len(cities) < number_teams:
            cities.extend(City.objects.all())
        while len(nicknames) < number_teams:
            nicknames.extend(Nickname.objects.all())
    elif level in ['pro', 'semipro', 'amateur']:
        level_filter = {}
        level_filter[level] = True
        while len(cities) < number_teams:
            cities.extend(City.objects.filter(**level_filter))
        while len(nicknames) < number_teams:
            nicknames.extend(Nickname.objects.filter(**level_filter))
    else:
        return HttpResponse("Invalid level for team creation.")
    shuffle(cities)
    shuffle(nicknames)
        
    coaches = [Coach(universe=universe,
                     first_name=names.first_name(),
                     last_name=names.last_name(),
                     skill=randint(60,90),
                     play_probabilities = json.dumps({}),
                     fg_dist_probabilities = json.dumps({})
                                       ) for x in xrange(int(number_teams))]
    for coach in coaches:
            coach.save()

    teams = [Team(universe=universe,
                  city=cities.pop(),
                  nickname=nicknames.pop(),
                  human_control=False,
                  home_field_advantage=randint(1,3),
                  draft_position_order = get_draft_position_order(),
                  coach = coaches.pop(),
                  playbook = Playbook.objects.get(id=1)) for x in xrange(int(number_teams))]
    Team.objects.bulk_create(teams)

    logger.info('{0} teams created in universe {1}'.format(number_teams, universe.name))