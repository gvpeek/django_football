import json
import pickle
import operator
import logging
import time

from collections import deque, OrderedDict
from random import choice, randint, shuffle
from ast import literal_eval

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max

import python_football

from .models import League, LeagueMembership, Game, Schedule, PlayoffTeams, Champions
from core.models import Universe, Year
from teams.models import Team, Roster, Playbook
from teams.utils import determine_number_pro_teams
from stats.models import TeamStats, GameStats
from stats.utils import update_stats, get_team_stats
# from people.views import practice_plays, call_play, choose_rush_pass_play

cached_team_names = {}

# used to convert model object to plain object to reduce db calls by taking advantange
# of cached values rather than foreign key lookups
class StandingsStats():
    def __init__(self, year, team_id, stats):
        self.year = year
        self.team_id = team_id,
        self.team =  get_team_name(team_id)
        self.pct  = stats.pct
        self.diff =  stats.diff
        self.score = stats.score
        self.wins =  stats.wins
        self.losses = stats.losses
        self.ties = stats.ties

def create_initial_universe_league(universe_id,
                  name,
                  level,
                  nbr_div=0):
    universe = Universe.objects.get(id=universe_id)
    year = Year.objects.get(universe=universe,current_year=True)
    universe_teams = Team.objects.filter(universe=universe)
    placed_teams = LeagueMembership.objects.filter(universe=universe,
                                                   year=year)
    available_teams = list(set(universe_teams) - set(placed_teams))
    available_teams = sorted(available_teams,key=operator.attrgetter('city.division'))
    divisions = create_divisions(available_teams, int(nbr_div))
    
    nbr_conf = len(divisions) / 2
    if nbr_conf:
        conferences = [[] for x in xrange(nbr_conf)]
    else:
        conferences = [[]]
        
    conf_ctr = 0
    for division in divisions:
            conferences[conf_ctr].append(division)
            if conf_ctr + 1 == len(conferences):
                conf_ctr = 0
            else:
                conf_ctr += 1
    
    league = League(universe=universe,
               name=name,
               level=level)
    league.save()
    
    conf_nbr=0
    total_divisions=0
    for conference in conferences:
            div_nbr=0
            for division in conference:
                    for team in division:
                            lm = LeagueMembership(universe=universe,
                                                  year=year,
                                                  league=league,
                                                  team=team,
                                                  conference=conf_nbr,
                                                  division=div_nbr)
                            lm.save()
                            ts = TeamStats(universe=universe,
                                           year=year,
                                           team=team)
                            ts.save()
                    div_nbr+=1
                    total_divisions+=1
            conf_nbr+=1

    league.number_playoff_teams = randint((total_divisions),(len(available_teams)/2))
    league.save()

def determine_nbr_div(nbr_teams):
    possible_div_sizes = [n for n in xrange(4,9) if not nbr_teams/n & 1]
    
    possible_nbr_divs = set(nbr_teams/x for x in possible_div_sizes)
   
    return choice(list(possible_nbr_divs))

def create_divisions(teams,nbr_div=None):
    divisions=[]
    nbr_teams=len(teams)
    if not nbr_div:
        nbr_div = determine_nbr_div(nbr_teams)

    if not nbr_div:
        nbr_div = 1

    teams_per_div=nbr_teams/nbr_div
    remainder=nbr_teams%nbr_div
    split_start=0
    split_end=0
    for x in xrange(nbr_div):
        split_end += teams_per_div
        if remainder:
            split_end += 1
            remainder -= 1
        divisions.append(teams[split_start:split_end])
        split_start=split_end
    return divisions
        
def create_schedule(league):
    year = Year.objects.get(universe=league.universe,
                            current_year=True)
    teams = LeagueMembership.objects.filter(universe=league.universe,
                                            year=year,
                                            league=league)
    structure = {}
    for team in teams:
        structure.setdefault(team.conference, {})
        structure[team.conference].setdefault(team.division, [])
        structure[team.conference][team.division].append(team.team)
        print structure

    total_weeks = 0
    schedule = []
    for conference, divisions in structure.iteritems():
        for div_nbr, division in divisions.iteritems():
            shuffle(division)
            anchor_team = None
            # 'balanced' will contain 1 if even number of teams, 0 if odd
            # used later to calculate number of weeks needed, since odd
            # numbered divisions require an extra week due to each team having a bye
            balanced = 1 - (len(division) % 2)
            print 'balanced', balanced, 'div len', len(division)
            nbr_weeks = len(division) - balanced
            max_weeks = 2 * nbr_weeks
            # To ensure all league teams play the same number of games
            # regardless of the number of teams in their division
            # capture the highest number of games played in a division
            # and apply that to all. The largest division should be 
            # processed first.
            if nbr_weeks > total_weeks:
                total_weeks = nbr_weeks
            else:
                nbr_weeks = total_weeks - balanced

            try:
                schedule[max_weeks]
            except:
                for x in xrange(max_weeks - len(schedule)):
                    schedule.append([])
            ## gpw is games per week
            gpw = len(division) / 2
            rotation1 = deque(division[:gpw])
            rotation2 = deque(division[gpw:])
            if balanced:
                anchor_team = rotation1.popleft()
            for week in range(nbr_weeks):
                if anchor_team:
                    schedule[week].append(Game(universe=league.universe,
                                               year=year,
                                               home_team=anchor_team, 
                                               away_team=rotation2[-1],
                                               use_overtime = True))
                    schedule[week+nbr_weeks].append(Game(universe=league.universe,
                                                         year=year,
                                                         home_team=rotation2[-1], 
                                                         away_team=anchor_team,
                                                         use_overtime = True))
                for team1, team2 in zip(rotation1,rotation2):
                    schedule[week].append(Game(universe=league.universe,
                                               year=year,
                                               home_team=team1,
                                               away_team=team2,
                                               use_overtime = True))
                    schedule[week+nbr_weeks].append(Game(universe=league.universe,
                                                         year=year,
                                                         home_team=team2,
                                                         away_team=team1,
                                                         use_overtime = True))

                rotation1.append(rotation2.pop())
                rotation2.appendleft(rotation1.popleft())

    for week in schedule:
        for game in week:
            game.save()
            db_schedule = Schedule(universe=league.universe,
                         year=year,
                         league=league,
                         game=game,
                         week=schedule.index(week) + 1,
                         game_number=week.index(game) + 1)
            db_schedule.save()

def copy_league_memberships(universe, source_year, new_year):
    logger = logging.getLogger('django.request')
    
    current_membership = LeagueMembership.objects.filter(universe=universe, year=source_year)
    for membership in current_membership:
        new_membership = LeagueMembership(universe=membership.universe,
                                          year=new_year,
                                          league=membership.league,
                                          team=membership.team,
                                          conference=membership.conference,
                                          division=membership.division)
        new_membership.save()

    logger.info('{0} current teams, {1} potential teams.'.format(len(current_membership), 
                                                                 determine_number_pro_teams(universe)))

def copy_rosters(universe, source_year, new_year):
    logger = logging.getLogger('django.request')
    
    current_rosters = Roster.objects.filter(universe=universe, year=source_year)
    for roster in current_rosters:
        roster.id = None
        roster.pk = None
        roster.year = new_year

        for position in roster.get_positions():
            player = getattr(roster,position)
            if player.retired:
                setattr(roster,position,None)
                setattr(roster,position+'_age',None)
                setattr(roster,position+'_rating',None)
                logger.info('{0} {1} {2} {3} {4} has retired.'.format(roster.team.city,
                                                                      roster.team.nickname,
                                                                      position,
                                                                      player.first_name,
                                                                      player.last_name))
            else:
                setattr(roster,position+'_age',player.age)
                setattr(roster,position+'_rating',player.ratings)
        roster.save()

def play_game(id, playoff=False):
    db_game = Game.objects.get(id=id)
    home_team = prepare_team_for_game(db_game.home_team, db_game.away_team, db_game)
    away_team = prepare_team_for_game(db_game.away_team, db_game.home_team, db_game)
    use_overtime=db_game.use_overtime or playoff
    number_of_overtime_periods = 0 if playoff else db_game.number_of_overtime_periods
    game = python_football.new_game(home_team=home_team, 
                                    away_team=away_team, 
                                    use_overtime=use_overtime,
                                    number_of_overtime_periods=number_of_overtime_periods)
    game.start_game()
    
    ## stores stats and returns losing team
    return update_stats(db_game, game, playoff)
        
    
def prepare_team_for_game(team, opponent, game):
    roster = Roster.objects.get(universe=game.universe,
                                year=game.year,
                                team=team)
    skills = {'qb': roster.qb_rating,
                     'rb': roster.rb_rating,
                     'wr': roster.wr_rating,
                     'ol': ((roster.og_rating + roster.c_rating + roster.ot_rating) / 3),
                     'dl': ((roster.dt_rating + roster.de_rating) / 2),
                     'lb': roster.lb_rating,
                     'cb': roster.cb_rating,
                     's': roster.s_rating,
                     'p': roster.p_rating,
                     'k': roster.k_rating,
                     'sp': roster.wr_rating}
    primary_color = team.primary_color
    secondary_color = team.secondary_color
    ## This is wonky. We have a JSON serialized object in the database, which is really a pickled object.
    ## TODO: investigate a better way to do this
    playbook = Playbook.objects.get(id=1)
    playbook = pickle.loads(json.loads(playbook.plays))
    
    coach = python_football.new_coach(skill=team.coach.skill)
    coach.practice_plays(playbook,skills)
    stats = python_football.new_statbook()
    team = python_football.new_team(city=team.city.name,
                                    nickname=team.nickname,
                                    skills=skills,
                                    primary_color=primary_color,
                                    secondary_color=secondary_color,
                                    playbook=playbook,
                                    stats=stats,
                                    coach=coach,
                                    home_field_advantage=team.home_field_advantage)
    
    return team

def scheduled_games_remaining(league):
    return Schedule.objects.filter(league=league,
                                    played=False).count()

def eliminate_playoff_team(league, team):
    year = Year.objects.get(universe=league.universe_id,
                            current_year=True)
    loser = PlayoffTeams.objects.get(universe=league.universe_id,
                                     year=year,
                                     league=league,
                                     team=team)
    loser.eliminated = True
    loser.save()

def play_game_batch(schedule_list):
    logger = logging.getLogger('django.request')
    
    start_time = time.time()
    for entry in schedule_list:
        loser = play_game(entry.game_id, entry.playoff_game)
        entry.played=True
        entry.save()
        if entry.playoff_game:
            eliminate_playoff_team(entry.league, loser)
    elapsed_time = time.time() - start_time
    logger.info('{0} games played in {1} seconds.'.format(len(schedule_list), elapsed_time))
        
    try:
        if entry:
            league=entry.league     
        if not scheduled_games_remaining(league):
            manage_playoffs(league)
    except UnboundLocalError, e:
        pass
        
def play_league_game(request, game_id):
    schedule_entry = Schedule.objects.get(game=game_id)
    
    play_game_batch([schedule_entry])
    
    return redirect('show_game_stats', game_id=game_id)

def play_league_week(request, league_id, week):
    schedule = Schedule.objects.filter(league=league_id,
                                    week=week,
                                    played=False)
                                    
    play_game_batch(schedule)
    
    return redirect('show_league_standings', league_id=league_id)

def play_league_remaining(request, league_id):
    schedule = Schedule.objects.filter(league=league_id,
                                    played=False)
                                    
    play_game_batch(schedule)
    
    return redirect('show_league_standings', league_id=league_id)

def play_season(league):
    play_unplayed_games(league)

def current_playoff_field_size(league):
    try:
        year = Year.objects.get(universe=league.universe,
                                current_year=True)
        return PlayoffTeams.objects.filter(universe = league.universe,
                                           year = year,
                                           league=league,
                                           eliminated=False).count()
    except ObjectDoesNotExist, e:
        return 0

def champion_determined(league):
    year = Year.objects.get(universe=league.universe,
                            current_year=True)
    return Champions.objects.filter(universe=league.universe,
                              year=year,
                              league=league).count()

def manage_playoffs(league):
    logger = logging.getLogger('django.request')
    
    year = Year.objects.get(universe=league.universe_id,
                            current_year=True)
    teams_remaining = current_playoff_field_size(league)
    if not teams_remaining:
        determine_playoff_field(league)
        teams_remaining = current_playoff_field_size(league)
    if teams_remaining == 1:
        if not champion_determined(league):
            remaining_team = PlayoffTeams.objects.get(universe = league.universe_id,
                                                      year = year,
                                                      league=league,
                                                      eliminated=False)
            champ = Champions(universe=league.universe,
                              year=year,
                              league=league,
                              team=remaining_team.team)
            champ.save()
            logger.info('The {0} {1} win {2} {3} Championship.'.format(champ.team.city, 
                                                                       champ.team.nickname,
                                                                       year.year,
                                                                       league.name))
            return False
        else:
            return False
        
    generate_playoff_schedule(league)
    
    
def determine_playoff_field(league):
    year = Year.objects.get(universe=league.universe_id,
                            current_year=True)
    sorted_standings = get_sorted_standings(league, year, True)

    division_winners=[]
    wild_card=[]

    for conference in sorted_standings:
        for div in conference:
            division_winners.append(div[0])
            wild_card.extend(div[1:])
        
    division_winners = sorted(division_winners, key=operator.attrgetter('pct', 'diff', 'score'), reverse=True)
    wild_card = sorted(wild_card, key=operator.attrgetter('pct', 'diff', 'score'), reverse=True)
    seed = 1
    for team in division_winners:
        pt = PlayoffTeams(universe = league.universe,
                          year = year,
                          league = league,
                          team = team.team,
                          seed = seed,
                          qualification = 'division')
        pt.save()
        seed += 1

    number_wild_card = league.number_playoff_teams - len(division_winners)
    for team in wild_card[:number_wild_card]:
        pt = PlayoffTeams(universe = league.universe,
                          year = year,
                          league = league,
                          team = team.team,
                          seed = seed,
                          qualification = 'wild_card')
        pt.save()
        seed += 1

def generate_playoff_schedule(league):
    year = Year.objects.get(universe=league.universe_id,
                            current_year=True)
    current_field = list(PlayoffTeams.objects.filter(universe=league.universe_id,
                                                     year=year,
                                                     league=league,
                                                     eliminated=False).order_by('seed'))

    current_round_teams=[]
    ## determine largest logical number of teams for current round
    ## increment by multiples of 2 until division == 1 - 2, 4, 8, 16, etc.
    s=2
    c=1
    while s > 1:
        c *= 2
        s=len(current_field) / c
    remainder = len(current_field) % c
    
    if remainder:
        cf_deque=deque(current_field)
        cf_deque.rotate(remainder*2)
        for x in xrange(remainder*2):
            current_round_teams.append(cf_deque.popleft())
    else:
        current_round_teams=current_field

    round_games=[]
    for x in xrange(len(current_round_teams)/2):
        round_games.append(Game(universe=league.universe,
                                year=year,
                                home_team=current_round_teams[x].team,
                                away_team=current_round_teams[-x-1].team,
                                use_overtime=True,
                                playoff_game = True))

    max_week = Schedule.objects.filter(universe=league.universe_id,
                                       year=year,
                                       league=league).aggregate(Max('week'))['week__max']
    for game in round_games:
        game.save()
        schedule = Schedule(universe=league.universe,
                     year=year,
                     league=league,
                     game=game,
                     week=max_week + 1,
                     game_number=round_games.index(game) + 1,
                     playoff_game=True)
        schedule.save()
             
def show_league_detail(request, league_id):
    league = League.objects.get(id=league_id)
    year = Year.objects.get(universe=league.universe_id,
                            current_year=True)
    membership_history = LeagueMembership.objects.filter(league=league)
    years = []
    for item in membership_history:
            years.append(item.year)
    
    template = loader.get_template('league_detail.html')
    context = RequestContext(request, {
            'league' : league,
            'years' : years,
            'league_teams' : [entry.team for entry in membership_history if entry.year == year],
    })
    
    return HttpResponse(template.render(context))

def get_team_name(team_id):
    logger = logging.getLogger('django.request')
    
    if not team_id in cached_team_names:
        try:
            team = Team.objects.get(id=team_id)
            cached_team_names[team_id] = team.city.name + ' ' + team.nickname
        except ObjectDoesNotExist, e:
            logger.error("Team ID {0} does not exist.".format(team_id))

    return cached_team_names.get(team_id)

def get_sorted_standings(league, year, return_team_object=False):
    members = LeagueMembership.objects.filter(universe=league.universe_id, year=year, league=league).order_by('conference', 'division')
    standings = []
    sorted_standings = []
    for item in members:
            try:
                    standings[item.conference]
            except:
                    standings.append([])
            try:
                    standings[item.conference][item.division]
            except:
                    standings[item.conference].append([])
            stats = get_team_stats(universe=league.universe, year=year, team=item.team)
            if return_team_object:
                standings[item.conference][item.division].append(stats)                
            else:
                standings_stats = StandingsStats(year.year, item.team_id, stats)
                standings[item.conference][item.division].append(standings_stats)

    for conference in standings:  
            sorted_standings.append([])
            ix = len(sorted_standings) - 1
            for division in conference:
                    sorted_standings[ix].append(sorted(division, key=operator.attrgetter('pct', 'diff', 'score'), reverse=True))

    return sorted_standings

def get_base_game_stat_display(entry, current_game):
    return {'id' : entry.game_id, 
            'played' : entry.played, 
            'teams' : [{'team' : get_team_name(current_game.away_team_id),
                        'period_score' : '',
                        'final' : ''}, 
                       {'team' : get_team_name(current_game.home_team_id),
                        'period_score' : '',
                        'final' : ''}]}

def show_standings(request, league_id, year=None):
    logger = logging.getLogger('django.request')
    
    start_time = time.time()
    league = League.objects.get(id=league_id)
    if year:
        year_obj = Year.objects.get(universe=league.universe_id, year=year)
    else:
        year_obj = Year.objects.get(universe=league.universe_id, current_year=True)
    sorted_standings = get_sorted_standings(league, year_obj)
    
    elapsed_time = time.time() - start_time
    logger.info("League {0} standings retrieved in {1} seconds".format(league.name, elapsed_time))
    

    ## get schedule and results
    start_time = time.time()
    schedule_id = None
    next_game_id = None
    schedule_results=OrderedDict()
    try:
        sched = Schedule.objects.filter(universe=league.universe_id, year=year_obj).order_by('week', 'game')
        for entry in sched:
            if not schedule_id:
                schedule_id = entry.id
            if entry.week not in schedule_results:
                schedule_results[entry.week] = []
            if not entry.played and not next_game_id:
                next_game_id = entry.game_id
            if entry.played:
                try:
                    current_game = entry.game
                    home_stats = GameStats.objects.get(universe=league.universe_id,
                                                       year=year_obj,
                                                       game=current_game,
                                                       team=current_game.home_team)
                    away_stats = GameStats.objects.get(universe=league.universe_id,
                                                       year=year_obj,
                                                       game=current_game,
                                                       team=current_game.away_team)
                    away={}
                    away['team'] = get_team_name(away_stats.team_id)
                    away['period_scores'] = literal_eval(away_stats.score_by_period)
                    away['final'] = away_stats.score
                    home={}
                    home['team'] = get_team_name(home_stats.team_id)
                    home['period_scores'] = literal_eval(home_stats.score_by_period)
                    home['final'] = home_stats.score
                    schedule_results[entry.week].append({'id' : entry.game_id, 
                                                         'played' : entry.played, 
                                                         'teams' : [away,home]})
                except ObjectDoesNotExist, e:
                    schedule_results[entry.week].append(get_base_game_stat_display(entry, entry.game))
            else:
                schedule_results[entry.week].append(get_base_game_stat_display(entry, entry.game))
        elapsed_time = time.time() - start_time
        logger.info("League {0} schedule retrieved in {1} seconds".format(league.name, elapsed_time))
            
    except Exception, e:
        print 'Error generating standings:' , e

    template = loader.get_template('standings.html')
    context = RequestContext(request, {
            'league' : league,
            'year' : year,
            'standings' : sorted_standings,
            'schedule' : schedule_results,
            'schedule_id' : schedule_id,
            'next_game_id' : next_game_id
    })
    return HttpResponse(template.render(context))
