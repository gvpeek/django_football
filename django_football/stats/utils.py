from ast import literal_eval

from django.core.exceptions import ObjectDoesNotExist

from .models import GameStats, TeamStats, PlayoffTeamStats
from leagues.models import PlayoffTeams

def get_game_stats(universe, year, game, team):
    try:
        gs = GameStats.objects.get(universe=universe,
                                   year=year,
                                   game=game,
                                   team=team)
    except ObjectDoesNotExist, e:
        gs = GameStats(universe=universe,
                       year=year,
                       game=game,
                       team=team)
        gs.save()
    return gs

def get_team_stats(universe, year, team, playoff=False):
    if not playoff:
        try:
            ts = TeamStats.objects.select_related('team').get(universe=universe,
                                                              year=year,
                                                              team=team)
        except ObjectDoesNotExist, e:
            ts = TeamStats(universe=universe,
                           year=year,
                           team=team)
            ts.save()
    else:
        try:
            ts = PlayoffTeamStats.objects.get(universe=universe,
                                              year=year,
                                              team=team)
        except ObjectDoesNotExist, e:
            ts = PlayoffTeamStats(universe=universe,
                                  year=year,
                                  team=team)
            ts.save()       
    return ts

def update_stats(db_game, game, playoff=False):
    home_db_game_stats = get_game_stats(db_game.universe, db_game.year, db_game, db_game.home_team)
    away_db_game_stats = get_game_stats(db_game.universe, db_game.year, db_game, db_game.away_team)
    home_db_team_stats = get_team_stats(db_game.universe, db_game.year, db_game.home_team, playoff)
    away_db_team_stats = get_team_stats(db_game.universe, db_game.year, db_game.away_team, playoff)
    home_game_stats = game.get_home_team().statbook.stats
    away_game_stats = game.get_away_team().statbook.stats
    stats = [[home_db_game_stats, home_db_team_stats, home_game_stats],
             [away_db_game_stats, away_db_team_stats, away_game_stats]]
                     
    loser = None
    if home_game_stats['score'] == away_game_stats['score']:
        home_db_team_stats.ties += 1
        away_db_team_stats.ties += 1
        home_db_game_stats.outcome = 'T'
        away_db_game_stats.outcome = 'T'
    elif home_game_stats['score'] > away_game_stats['score']:
        home_db_team_stats.wins += 1
        away_db_team_stats.losses += 1
        home_db_game_stats.outcome = 'W'
        away_db_game_stats.outcome = 'L'
        loser = db_game.away_team
    else:
        home_db_team_stats.losses += 1
        away_db_team_stats.wins += 1
        home_db_game_stats.outcome = 'L'
        away_db_game_stats.outcome = 'W'
        loser = db_game.home_team

    home_db_team_stats.opp += away_game_stats['score']
    away_db_team_stats.opp += home_game_stats['score']

    for db_game_stats, db_team_stats, game_stats in stats:
        for key, game_value in game_stats.iteritems():
            db_team_value = getattr(db_team_stats,key)
            ## @TODO fix this to check type
            if key == 'completion_pct':
                    db_team_value = float(db_team_value)
            ## @TODO fix this to check type
            if key == 'score_by_period':
                    db_team_value = literal_eval(db_team_value)
                    while len(db_team_value) < len(game_value):
                            db_team_value.append(0)
                    db_team_value = [x+y for x,y in zip(db_team_value,game_value)]
            else:
                    db_team_value += game_value
            setattr(db_game_stats,key,game_value)
            setattr(db_team_stats,key,db_team_value)
        db_team_stats.pct = (db_team_stats.wins + (db_team_stats.ties / 2.0)) / (float(db_team_stats.wins + db_team_stats.losses + db_team_stats.ties))
        db_team_stats.completion_pct = (db_team_stats.pass_comp / float(db_team_stats.pass_att))
        db_team_stats.diff = db_team_stats.score - db_team_stats.opp
        db_game_stats.save()
        db_team_stats.save()
        
    return loser