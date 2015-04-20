from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.exceptions import ObjectDoesNotExist

from .models import Team, Roster
from core.models import Year
from leagues.models import Game, Schedule, Champions, PlayoffTeams
from stats.models import GameStats, TeamStats

def get_game_outcome(game, team, opponent):
    try:
        team_stats = GameStats.objects.get(universe=game.universe,
                                           year=game.year,
                                           game=game,
                                           team=team)
        opp_stats = GameStats.objects.get(universe=game.universe,
                                           year=game.year,
                                           game=game,
                                           team=opponent)
    except ObjectDoesNotExist, e:
        return False
                                       
    return {'outcome' : team_stats.outcome,
            'score' : team_stats.score,
            'opp' : opp_stats.score}

def show_team_detail(request, team_id, year):
        team = Team.objects.get(id=team_id)
        year_obj = Year.objects.get(universe=team.universe, year=year)
        roster = Roster.objects.get(universe=team.universe, team=team, year=year_obj)
        roster_list = [(roster.qb, roster.qb_age, roster.qb_rating),
                  (roster.rb, roster.rb_age, roster.rb_rating),
                  (roster.wr, roster.wr_age, roster.wr_rating),
                  (roster.og, roster.og_age, roster.og_rating),
                  (roster.c, roster.c_age, roster.c_rating),
                  (roster.ot, roster.ot_age, roster.ot_rating),
                  (roster.de, roster.de_age, roster.de_rating),
                  (roster.dt, roster.dt_age, roster.dt_rating),
                  (roster.lb, roster.lb_age, roster.lb_rating),
                  (roster.cb, roster.cb_age, roster.cb_rating),
                  (roster.s, roster.s_age, roster.s_rating),
                  (roster.k, roster.k_age, roster.k_rating),
                  (roster.p, roster.p_age, roster.k_rating)]

        league_schedule = Schedule.objects.filter(universe=team.universe, year=year_obj).order_by('week', 'game')
        team_schedule = {}
        weeks = set()
        for entry in league_schedule:
            outcome = None
            if not entry.playoff_game:
                weeks.add(entry.week)
            if team == entry.game.home_team:
                outcome = get_game_outcome(entry.game, entry.game.home_team, entry.game.away_team)
                team_schedule[entry.week] = {'opponent' : str(entry.game.away_team.city) + ' ' + entry.game.away_team.nickname}
            elif team == entry.game.away_team:
                outcome = get_game_outcome(entry.game, entry.game.away_team, entry.game.home_team)
                team_schedule[entry.week] = {'opponent' : 'at ' + str(entry.game.home_team.city) + ' ' + entry.game.home_team.nickname}
            if outcome:
                team_schedule[entry.week]['outcome'] = outcome['outcome'] + ' ' + str(outcome['score']) + '-' + str(outcome['opp'])
            elif entry.week in team_schedule and not team_schedule[entry.week].get('outcome',''):
                team_schedule[entry.week]['outcome'] = ''
        
        for week in weeks:
            if week not in team_schedule:
                team_schedule[week] = {'opponent' : 'Bye', 'outcome' : ''}
                
        print team_schedule

        template = loader.get_template('team_detail.html')
        context = RequestContext(request, {
                'team' : team,
                'roster' : roster_list,
                'team_schedule' : team_schedule
        })
        return HttpResponse(template.render(context)) 
        
def show_team_history(request, team_id):
    team = Team.objects.get(id=team_id)
    team_stats = TeamStats.objects.filter(team=team_id).order_by('year')
    championship_years = [champion.year.year for champion in Champions.objects.select_related().filter(team=team_id)]
    playoff_years = {playoff.year.year : playoff.seed for playoff in PlayoffTeams.objects.select_related().filter(team=team_id)}
    print playoff_years
    team_rosters = None
    
    template = loader.get_template('team_history.html')
    context = RequestContext(request, {
            'team' : team,
            'team_stats' : team_stats,
            'team_roaters' : team_rosters,
            'championship_years' : championship_years,
            'playoff_years' : playoff_years,
    })
    return HttpResponse(template.render(context))