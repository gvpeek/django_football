import logging

from ast import literal_eval

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.exceptions import ObjectDoesNotExist

from .models import GameStats
from leagues.models import Game, Schedule

logger = logging.getLogger('django.request')

def game_stats(request, game_id):
    game = Game.objects.get(id=game_id)
    team_stats = GameStats.objects.filter(game=game)
    try:
        league_id = Schedule.objects.get(game=game).league.id
    except ObjectDoesNotExist, e:
        logger.info('Stats being retrieved for a game not associated with a league.')
    
    if team_stats.first().team_id == game.home_team_id:
        home_team_stats = team_stats.first()
        away_team_stats = team_stats.last()
    else:
        home_team_stats = team_stats.last()
        away_team_stats = team_stats.first()
        
    home_score_by_period = literal_eval(home_team_stats.score_by_period)
    home_score_by_period.append(home_team_stats.score)
    away_score_by_period = literal_eval(away_team_stats.score_by_period)
    away_score_by_period.append(away_team_stats.score)
    
    display_stats = ['total_yards', 'pass_att',  'pass_comp', 'completion_pct', 
                    'pass_yards', 'pass_td',  'intercepted', 'sacked', 'rush_att', 
                    'rush_yards', 'rush_td', 'fumbles', 'fg_att', 'fg', 'xp_att',
                    'xp', 'conv_att', 'conv', 'punts', 'punt_yards', 'punt_touchbacks',
                    'punt_blocks', 'punt_returns', 'punt_return_yards', 'kickoffs',
                    'kickoff_yards', 'kickoff_touchbacks', 'kick_returns',
                    'kick_return_yards', 'safeties']
                    
        
    template = loader.get_template('game_stats.html')
    context = RequestContext(request, {
        'universe_id' : game.universe_id,
        'year' : game.year.year,
        'league_id' : league_id,
        'home_team_stats' : home_team_stats,
        'home_score_by_period' : home_score_by_period,
        'away_team_stats' : away_team_stats,
        'away_score_by_period' : away_score_by_period,
        'display_stats' : display_stats
    })
    return HttpResponse(template.render(context))

