from random import randint

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from .models import Universe, Year
from .forms import CreateUniverseForm

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
        # seed_universe_players(u,1500)

        # # TODO move this to an initialize method
        # # TODO investigate better way of testing presence of data
        # try:
        #     Playbook.objects.get(id=1)
        # except:
        #     create_playbook(request)
        # try:
        #     City.objects.get(id=1)
        # except:
        #     initialize_cities(request)
        # try:
        #     Nickname.objects.get(id=1)
        # except:
        #     initialize_nicknames(request)
        # create_teams(request, u, 'pro')
        # create_league(request, u.id, choice(league_names), 'pro')
        
        return HttpResponse("Universe %s created." % name)
        
def year_create(universe, year=None):
        year = Year(universe=universe,
                         year=year)
        year.save()
        
        return year