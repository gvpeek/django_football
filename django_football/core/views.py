import logging
import time

from random import randint, choice

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from .models import Universe, Year
from .forms import CreateUniverseForm
from people.views import seed_universe_players, draft_players
from teams.utils import initialize_team_source_data, create_initial_universe_teams
from leagues.views import create_initial_universe_league, create_schedule
from leagues.models import League

def index(request):
    universe_list = Universe.objects.all()
    template = loader.get_template('index.html')
    context = RequestContext(request, {
            'universe_list' : universe_list,
    })
    return HttpResponse(template.render(context))

def universe_create(request):
    logger = logging.getLogger('django.request')
    
    league_names  = ['AFL', 'NFL', 'CFL', 'NAFL', 'UFL', 'USFL', 'NFA', 'WFL', 'IFL']
    form = CreateUniverseForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
    universe = Universe(name=name)
    universe.save()
    logger.info("Universe {0} created".format(name))
    year_create(universe, randint(1940,2010))
    
    start_time = time.time()
    seed_universe_players(universe,400)
    elapsed_time = time.time() - start_time
    logger.info("Universe {0} players seeded in {1} seconds".format(name, elapsed_time))
    
    initialize_team_source_data()

    create_initial_universe_teams(universe, 'pro')
    create_initial_universe_league(universe.id, choice(league_names), 'pro')
    year_start(universe)
    
    universe_list = Universe.objects.all()
    template = loader.get_template('index.html')
    context = RequestContext(request, {
            'universe_list' : universe_list,
    })
    return HttpResponse(template.render(context))
        
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
        
def show_leagues(request, universe_id):
        universe = Universe.objects.get(id=universe_id)
        leagues = League.objects.filter(universe=universe)
        
        template = loader.get_template('league_list.html')
        context = RequestContext(request, {
                'universe' : universe.name,
                'league_list' : leagues,
        })
        
        return HttpResponse(template.render(context))