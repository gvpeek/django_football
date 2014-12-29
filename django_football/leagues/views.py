import operator

from collections import deque
from random import choice, randint, shuffle

from django.shortcuts import render

from .models import League, LeagueMembership, Game, Schedule
from core.models import Universe, Year
from teams.models import Team, Roster


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
                    div_nbr+=1
            conf_nbr+=1

    league.number_playoff_teams = randint((div_nbr+1),(len(available_teams)/2))
    league.save()

    # play_season(league)
    # play_playoffs(league)

def determine_nbr_div(nbr_teams):
    possible_div_sizes = [n for n in xrange(4,9) if not nbr_teams/n & 1]
    
    possible_nbr_divs = set(nbr_teams/x for x in possible_div_sizes)
    
    print 'poss_div_size', possible_div_sizes, 'poss_nbr_divs', possible_nbr_divs
   
    return choice(list(possible_nbr_divs))

def create_divisions(teams,nbr_div=None):
    divisions=[]
    nbr_teams=len(teams)
    if not nbr_div:
        nbr_div = determine_nbr_div(nbr_teams)

    print nbr_div
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

def play_game(id, playoff=False):
    g = Game.objects.get(id=id)
    add_fields_to_team(g.home_team, g)
    add_fields_to_team(g.away_team, g)
    game = GameDay(home_team=g.home_team, 
                   away_team=g.away_team, 
                   use_overtime=g.use_overtime)
    game.start_game()
    update_stats(g, game, playoff)

def play_unplayed_games(league, playoff=False):
    year = Year.objects.get(universe=league.universe,
                            current_year=True)
    schedule = Schedule.objects.filter(universe=league.universe,
                                       year=year,
                                       league=league,
                                       played=False)

    for game in schedule:
        play_game(game.game.id, playoff)
        game.played = True
        game.save()
        if playoff:
            game_stats = GameStats.objects.filter(game=game.game.id)
            print game_stats, game_stats[0].team, game_stats[0].score, game_stats[0].outcome, \
                              game_stats[1].team, game_stats[1].score, game_stats[1].outcome
            loser = None
            for team in game_stats:
                if team.outcome == 'L':
                    if not loser:
                        loser = team.team
                    else:
                        raise Exception('More than one playoff loser found ' + team.team + ' & ' + loser)
            if not loser:
                raise Exception('Playoff winner could not be determined')
            # if game_stats[0].score >  game_stats[1].score:
            #     loser = game_stats[1].team
            # elif  game_stats[0].score <  game_stats[1].score:
            #     loser = game_stats[0].team
            # else:
            #     raise Exception("No winner in playoff game_stats")

            pt = PlayoffTeams.objects.get(universe=league.universe,
                                          year=year,
                                          league=league,
                                          team=loser)
            pt.eliminated = True
            pt.save()

def play_season(league):
    play_unplayed_games(league)

def determine_playoff_field(league):
    year = Year.objects.get(universe=league.universe,
                            current_year=True)
    sorted_standings = get_sorted_standings(league, year)

    division_winners=[]
    wild_card=[]

    for conference in sorted_standings:
        for div in conference:
            print 'div sort', div
            division_winners.append(div[0])
            wild_card.extend(div[1:])
        
    division_winners = sorted(division_winners, key=operator.attrgetter('pct', 'diff', 'score'), reverse=True)
    wild_card = sorted(wild_card, key=operator.attrgetter('pct', 'diff', 'score'), reverse=True)
    print 'div' , division_winners
    print 'wild', wild_card
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
    year = Year.objects.get(universe=league.universe,
                        current_year=True)
    current_field = list(PlayoffTeams.objects.filter(universe=league.universe,
                                            year=year,
                                            league=league).filter(eliminated=False).order_by('seed'))
    
    if len(current_field) == 1:
        champ = Champions(universe=league.universe,
                          year=year,
                          league=league,
                          team=current_field[0].team)
        champ.save()
        return False

    current_round_teams=[]
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

    max_week = Schedule.objects.filter(universe=league.universe,
                                    year=year,
                                    league=league).aggregate(Max('week'))['week__max']
    for game in round_games:
        game.save()
        schedule = Schedule(universe=league.universe,
                     year=year,
                     league=league,
                     game=game,
                     week=max_week + 1,
                     game_number=round_games.index(game) + 1)
        schedule.save()

    return True

def play_playoffs(league):
    playoff_teams = determine_playoff_field(league)
    while generate_playoff_schedule(league):
        play_unplayed_games(league,playoff=True)
              
def add_fields_to_team(team, game):
        roster = Roster.objects.get(universe=game.universe,
                                    year=game.year,
                                    team=team)
        team.skills = {'qb': roster.qb_rating,
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
        team.primary_color = (randint(0,255),randint(0,255),randint(0,255))
        team.secondary_color = (randint(0,255),randint(0,255),randint(0,255))
        p = Playbook.objects.get(id=1)
        p = json.loads(p.plays)
        p = pickle.loads(p)
        team.plays = p
        team.coach.practice_plays(team.coach,team.plays,team.skills)
        team.coach.save()
        team.coach.play_probabilities = json.loads(team.coach.play_probabilities)
        team.coach.fg_dist_probabilities = json.loads(team.coach.fg_dist_probabilities)
        team.stats = StatBook()

def show_leagues(request, universe_id):
        universe = Universe.objects.get(id=universe_id)
        leagues = League.objects.filter(universe=universe)
        
        template = loader.get_template('football/league_list.html')
        context = RequestContext(request, {
                'universe' : universe.name,
                'league_list' : leagues,
        })
        
        return HttpResponse(template.render(context))

def show_league_detail(request, league_id):
        league = League.objects.get(id=league_id)
        membership_history = LeagueMembership.objects.filter(league=league)
        years = []
        for item in membership_history:
                years.append(item.year)
        
        template = loader.get_template('football/league_detail.html')
        context = RequestContext(request, {
                'league' : league,
                'years' : years,
        })
        
        return HttpResponse(template.render(context))

def get_sorted_standings(league, year):
    members = LeagueMembership.objects.filter(universe=league.universe, year=year, league=league).order_by('conference', 'division')
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
            stats = TeamStats.objects.get(universe=item.universe, year=item.year, team=item.team)
            standings[item.conference][item.division].append(stats)

    for conference in standings:  
            sorted_standings.append([])
            ix = len(sorted_standings) - 1
            for division in conference:
                    sorted_standings[ix].append(sorted(division, key=operator.attrgetter('pct', 'diff', 'score'), reverse=True))

    return sorted_standings

def show_standings(request, league_id, year):
        league = League.objects.get(id=league_id)
        year_obj = Year.objects.get(universe=league.universe, year=year)
        
        sorted_standings = get_sorted_standings(league, year_obj)

        schedule_results=[]
        try:
            games = Game.objects.filter(universe=league.universe, year=year_obj).order_by('id')
            for idx, game in enumerate(games):
                    try:
                        home_stats = GameStats.objects.get(universe=game.universe,
                                                             year=game.year,
                                                             game=game,
                                                             team=game.home_team)
                        away_stats = GameStats.objects.get(universe=game.universe,
                                                             year=game.year,
                                                             game=game,
                                                             team=game.away_team)
                        away=[]
                        away.extend([away_stats.team])
                        away.extend(literal_eval(away_stats.score_by_period))
                        away.extend([away_stats.score])
                        home=[]
                        home.extend([home_stats.team])
                        home.extend(literal_eval(home_stats.score_by_period))
                        home.extend([home_stats.score])
                        schedule_results.append([away,home])
                    except:
                        schedule_results.append([[game.away_team],[game.home_team]])
        except Exception, e:
            print 'Error generating standings:' , e

        template = loader.get_template('football/standings.html')
        context = RequestContext(request, {
                'league_name' : league.name,
                'year' : year,
                'standings' : sorted_standings,
                'schedule' : schedule_results,
        })
        return HttpResponse(template.render(context))
