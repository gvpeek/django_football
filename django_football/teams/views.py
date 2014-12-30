from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from .models import Team, Roster
from core.models import Year

def show_roster(request, team_id, year):
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
        template = loader.get_template('roster.html')
        context = RequestContext(request, {
                'team' : team,
                'roster' : roster_list,
        })
        return HttpResponse(template.render(context)) 