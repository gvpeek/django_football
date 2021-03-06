import logging
import time

from random import randint, choice

from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import RequestContext, loader

from .models import Universe, Year
from .forms import CreateUniverseForm
from people.views import seed_universe_players, draft_players, age_players, create_players
from people.tasks import calculate_future_ratings, sign_players
from teams.utils import initialize_team_source_data, create_initial_universe_teams
from leagues.views import (create_initial_universe_league, create_schedule, 
                           copy_league_memberships, copy_rosters, champion_determined)
from leagues.models import League

def index(request):
    form = CreateUniverseForm()
    universe_list = Universe.objects.all()
    template = loader.get_template('index.html')
    context = RequestContext(request, {
        'form' : form,
        'universe_list' : universe_list,
    })
    return HttpResponse(template.render(context))

def universe_create(request):
    logger = logging.getLogger('django.request')
    
    league_names  = ['AFL', 'NFL', 'CFL', 'NAFL', 'UFL', 'USFL', 'NFA', 'WFL', 'IFL']
    form = CreateUniverseForm(request.POST)
    universe = form.save()
    logger.info("Universe {0} created".format(universe.name))
    year_create(universe, randint(1940,2010))
    
    start_time = time.time()
    seed_universe_players(universe,universe.new_players_per_year)
    elapsed_time = time.time() - start_time
    logger.info("Universe {0} players seeded in {1} seconds".format(universe.name, elapsed_time))
    
    initialize_team_source_data()

    create_initial_universe_teams(universe, 'pro')
    create_initial_universe_league(universe.id, choice(league_names), 'pro')
    year_start(universe)

    calculate_future_ratings.delay(universe)

    return redirect('index')

        
def year_create(universe, year=None):
    year = Year(universe=universe,
                year=year)
    year.save()
    
    return year
        
def year_start(universe):
    draft_players(universe)
    leagues = League.objects.filter(universe=universe)
    for league in leagues:
        create_schedule(league)

def create_year(universe, year):
        year.current_year = False
        year.save()
        new_year = Year(universe=universe,
                         year=year.year + 1)
        new_year.save()
        
        return new_year

def advance_year(request,universe_id):
        logger = logging.getLogger('django.request')
        
        universe = Universe.objects.get(id=universe_id)
        ## putting this in an if condition so we don't execute a save if we don't need to
        if universe.new_player_delta_per_year:
            universe.new_players_per_year += universe.new_player_delta_per_year
            universe.save()
            
        year = Year.objects.get(universe=universe,current_year=True)
        new_year = create_year(universe, year)

        start_time = time.time()
        age_players(universe)
        elapsed_time = time.time() - start_time
        logger.info("Universe {0} players aged in {1} seconds".format(universe.name, elapsed_time))

        start_time = time.time()        
        create_players(universe, universe.new_players_per_year)
        elapsed_time = time.time() - start_time
        logger.info("Universe {0} players created in {1} seconds".format(universe.name, elapsed_time))

        start_time = time.time()
        copy_league_memberships(universe, year, new_year)
        elapsed_time = time.time() - start_time
        logger.info("Universe {0} league membership copied in {1} seconds".format(universe.name, elapsed_time))

        start_time = time.time()      
        copy_rosters(universe, year, new_year)
        elapsed_time = time.time() - start_time
        logger.info("Universe {0} rosters copied in {1} seconds".format(universe.name, elapsed_time))

        start_time = time.time()
        sign_players(universe, new_year)
        elapsed_time = time.time() - start_time
        logger.info("Universe {0} players signed in {1} seconds".format(universe.name, elapsed_time))

        start_time = time.time()
        draft_players(universe)
        elapsed_time = time.time() - start_time
        logger.info("Universe {0} players drafted in {1} seconds".format(universe.name, elapsed_time))

        leagues = League.objects.filter(universe=universe)

        start_time = time.time()
        for league in leagues:
                create_schedule(league)
        elapsed_time = time.time() - start_time
        logger.info("Universe {0} league schedules created in {1} seconds".format(universe.name, elapsed_time))
        return redirect('show_leagues', universe_id=universe_id)

def show_leagues(request, universe_id):
        universe = Universe.objects.get(id=universe_id)
        leagues = League.objects.filter(universe=universe)
        
        season_complete = True
        for league in leagues:
            if not champion_determined(league):
                season_complete = False
                break
        
        template = loader.get_template('league_list.html')
        context = RequestContext(request, {
                'universe' : universe,
                'league_list' : leagues,
                'season_complete' : season_complete
        })
        
        return HttpResponse(template.render(context))