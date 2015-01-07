import json
import logging

from math import floor, ceil, pow
from random import randint, choice, shuffle
from copy import deepcopy

from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from .models import Player
from core.models import Year
from stats.models import TeamStats
from teams.models import Team, Roster

import names

# TODO see if processing speed increases by converting stub to dictionary, removing need for string & int translations
def create_player_stub(number):
    ''' player attributes are concatenated into a string which is used to track each player stub
    '''
    players = ['11' + str(randint(25,40)) +
               str(int((floor(((32 * 100) * pow(randint(5,100),-.5)) / 100) + 18))) +
               str(randint(1,4)) +
               str(randint(3,5)) +
               'A' +
               choice(['QB','RB','WR','OT','OG','C','DT','DE','LB','CB','S','K','P'])
                   for x in xrange(int(number))]

    return players

def _check_rating_range_stub(rating, rating_range, status):
    ''' function to check if player is within the rating range for their given age range. If a player
        is below the minimum range, they retire. If a player is above the maximum range, their rating
        is set to the maximum.
    '''
    if rating < min(rating_range):
        status = 'R'
    elif rating > max(rating_range):
        rating = max(rating_range)
    return rating, status

def age_player_stub(player_data, years=1):
    ''' function to break apart player stub and age them a single year
    '''
    min_max_ratings = [(14,(20,50)), # (age, (min,max))
                       (18,(30,60)),
                       (22,(45,75)),
                       (99,(60,90))]
    age, rating, apex, inc, dec, status, position = (int(player_data[:2]), 
                                                     int(player_data[2:4]), 
                                                     int(player_data[4:6]),
                                                     int(player_data[6]),
                                                     int(player_data[7]),
                                                     player_data[8],
                                                     player_data[9:])
    for y in xrange(int(years)):        
        age += 1
        if age <= apex:
            rating += randint(1,inc)
        else:
            rating -= randint(3,dec)
        for range_max,ratings in min_max_ratings:
            if age <= range_max:
                rating, status = _check_rating_range_stub(rating, ratings, status)
                break
        return str(age)+str(rating)+str(apex)+str(inc)+str(dec)+status+position

def seed_universe_players(universe, players_per_year):
    ''' This is a function to create, in bulk, the initial set of players for a given universe. Since the players 
        will not be referenced, a stub of necessary attributes is used in this process. The player stubs are "aged" for 
        50 years, with the remaining unretired players being instantiated into full player records and stored in 
        the database.
    '''

    # Main Logic
    logger = logging.getLogger('django.request')
    
    pl=[]
    for x in xrange(50):
        pl = [age_player_stub(player) for player in pl]        
        pl = [player for player in pl if player[8] != 'R']
        pl.extend(create_player_stub(players_per_year))

    players=[]
    for p in pl:
        age, rating, apex, inc, dec, status, position = (int(p[:2]), 
                                                         int(p[2:4]), 
                                                         int(p[4:6]),
                                                         int(p[6]),
                                                         int(p[7]),
                                                         p[8],
                                                         p[9:])
        players.extend([Player(universe=universe,
                               first_name=names.first_name(),
                               last_name=names.last_name(),
                               age = age,
                               position = position,
                               constitution = randint(25,40),
                               retired = False,
                               apex_age = apex,
                               growth_rate = inc,
                               declination_rate = dec,
                               ratings = rating)])

    Player.objects.bulk_create(players)
    
    logger.info('{0} players created in universe {1}.'.format(len(players), universe.name))


def determine_draft_needs(preference, roster):
        filled=[]
        for position in preference:
                if getattr(roster, position.lower()):
                        filled.append(position)
        shuffle(filled)
        for position in filled:
                preference.remove(position)
                preference.append(position)
                
        return preference
    
def draft_players(universe):
    current_year = Year.objects.get(universe=universe,
                                    current_year=True)
    previous_year=None
    try:
        previous_year = Year.objects.get(universe=universe,
                                         year=(current_year.year - 1))
    except ObjectDoesNotExist, e:
        print 'No previous year - ', e

    teams=[]
    try:
        team_order=TeamStats.objects.filter(universe=universe,
                                          year=previous_year).order_by('pct')
        for team_stat in team_order:
            teams.append(list(Team.objects.get(id=team_stat.team.id))[0])
    except ObjectDoesNotExist, e:
        print 'No previous team stats - ', e

    if not teams:
        teams = Team.objects.filter(universe=universe)
        shuffle(list(teams))
    draft_preference = {}
    nbr_positions = 0 
    for team in teams:
        try:
            r = Roster.objects.get(universe=universe,
                                   year=current_year,
                                   team=team)
        except:
            r = Roster(universe=universe,
                       year=current_year,
                       team=team)
            r.save()
            
        draft_preference[team] = deepcopy(json.loads(team.draft_position_order))
        draft_preference[team] = determine_draft_needs(draft_preference[team], r)
        if nbr_positions < len(draft_preference[team]):
                nbr_positions=len(draft_preference[team])
                
    draft_order=[]
    for i in xrange(nbr_positions):
        for team in teams:
            try:
                draft_order.append((team, draft_preference[team][i]))
            except:
                pass
                        
    for pick_team, pick_position in draft_order:
        players = Player.objects.filter(universe=universe,
                                        position=pick_position,
                                        retired=False,
                                        signed=False,
                                        age__gte=23).order_by('ratings').reverse()
        roster = Roster.objects.get(universe=universe,
                                    year=current_year,
                                    team=pick_team)
        player = players[0]
        current_player = getattr(roster, pick_position.lower())
        if not current_player or \
                (player.ratings >  current_player.ratings): # and player.age < current_player.age 
            # current_player = Player.objects.get(id=roster.pick_position.lower().id)
            if current_player:
                current_player.signed=False
                current_player.save()
            setattr(roster,pick_position.lower(),player)
            setattr(roster,pick_position.lower()+'_age',player.age)
            setattr(roster,pick_position.lower()+'_rating',player.ratings)
            roster.save()
            player.signed=True
            player.save()

## Coach functions
def practice_plays(coach,playbook,skills):
#        results = namedtuple('PracticeResults',['id','runs','success','total_yardage','success_yardage','turnover'])
    play_outcomes = {}
    fg_outcomes = {}
    for play in playbook:
        runs=[]
        success=0
        total_yardage=0
        success_yardage=0
        turnover=0
        if (play.is_rush() or play.is_pass()) and not play.id=='RC':
            for x in range(coach.skill):
                yds,trn = play.run(skills,{'dl':50,'lb':50,'cb':50,'s':50},0)
                if trn:
                    turnover += 1
                    yds=-20
                elif yds > 0:
                    success += 1
                    success_yardage += yds
                runs.append(yds)
            total_yardage = sum(runs)
            play_outcomes[play.id]={k: (len([i for i in runs if i >= k])/float(len(runs)))*100 for k in range(1,52)}
        elif play.is_field_goal():
                kicks=[]
                for x in range((coach.skill / 2)):
                    yds,trn = play.run(skills,{'sp':50},0)
                    kicks.append(yds)
                max_dist = max(kicks)
                fg_outcomes={k: (len([i for i in kicks if i >= k])/float(len(kicks)))*100 for k in range(1,61)}
    print 'plays', play_outcomes
    print
    print 'fg', fg_outcomes
    return {'play_probabilities' : json.dumps(play_outcomes),
            'fg_probabilities' : json.dumps(fg_outcomes)}
                    
def call_play(available_plays,
              state,
              down_distance,
              score_difference,
              period,
              time_remaining,
              distance_to_endzone):
    ## 
    ## to sort list of namedtupes: 
    ## in place - list.sort(key=lambda tup: tup.success,reverse=True)
    ## sorted_list = sorted(list, key=lambda tup: tup.success,reverse=True)
    play_choice=None
    target_yards=None
    curr_period,tot_periods=period(True)
    periods_left=tot_periods - curr_period
    if periods_left < 0:
        periods_left=0
    time,period_length=time_remaining(True)
    total_time_remaining= (time.total_seconds() + (periods_left*period_length.total_seconds()))
    if total_time_remaining > 0:
        time_score_ratio=(score_difference()/(total_time_remaining/30.0))
    urgency_threshold=-.4
        
    if state().is_drive():
        down, dist = down_distance()
        if down in [1,2,3] or (down==4 and urgency_threshold > time_score_ratio):
            if urgency_threshold > time_score_ratio:
                target_yards=ceil(distance_to_endzone()/2)
            elif down in [1,2]:
                target_yards=ceil(dist/2)
            elif down == 3:
                target_yards=dist
            play_choice=self.choose_rush_pass_play(available_plays, target_yards)
        elif down == 4:
            try:
                distance=unicode(int(distance_to_endzone()))
                if self.fg_dist_probabilities.get(distance) >= 40:
                    play_choice=available_plays['FG']
            except:
                pass
            if not play_choice:
                play_choice=available_plays['PUNT']
    elif state().is_conversion():
        if score_difference in [-2,-5,-10,-16,-17,-18] and (urgency_threshold > time_score_ratio or not total_time_remaining):
            play_choice=self.choose_rush_pass_play(available_plays, target_yards)
        else:
            play_choice=available_plays['XP']
    elif state().is_kickoff():
        if urgency_threshold > time_score_ratio:
            play_choice=available_plays['OK']
        else:
            play_choice=available_plays['K']
    elif state().is_free_kick():
        play_choice=available_plays['K']
    
    if not play_choice:
        play_choice = choice(available_plays.values())

    return play_choice

def choose_rush_pass_play(self,
                          available_plays,
                          target_yards):
    target=unicode(int(target_yards))
    play_choice=None
    choices=[]
    success_rates = []
    for play in self.play_probabilities:
        int_play = int(play)

        if int_play in available_plays:
            try:
                success_rates.append(self.play_probabilities[play].get(target))
                choices.append(available_plays[int_play])
            except:
                print 'play call error', sys.exc_info()[0]

    if len(success_rates) and sum(success_rates):
        avg=sum(success_rates)/float(len(success_rates))
        try:
            prob=[((item / avg) /float(len(success_rates))) for item in success_rates]
        except:
            print item, avg, float(len(success_rates)), play, target_yards
        
        r = random()
        running_total=0
        for step in prob:
            # print running_total, r
            if running_total < r < (running_total + step):
                play_choice = choices[prob.index(step)]
                # print 'play_selected', play_choice
                break
            running_total += step
            
    return play_choice