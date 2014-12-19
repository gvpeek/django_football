from random import randint, choice

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from .models import Universe, Year
from .forms import CreateUniverseForm
from people.views import seed_universe_players
from teams.utils import initialize_team_source_data, create_initial_universe_teams

def index(request):
        universe_list = Universe.objects.all()
        template = loader.get_template('index.html')
        context = RequestContext(request, {
                'universe_list' : universe_list,
        })
        return HttpResponse(template.render(context))

def universe_create(request):
        league_names  = ['AFL', 'NFL', 'CFL', 'NAFL', 'UFL', 'USFL', 'NFA', 'WFL', 'IFL']
        form = CreateUniverseForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
        universe = Universe(name=name)
        universe.save()
        year_create(universe, randint(1940,2010))
        seed_universe_players(universe,1500)
        
        initialize_team_source_data()

        create_initial_universe_teams(universe, 'pro')
        # create_league(request, u.id, choice(league_names), 'pro')
        
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