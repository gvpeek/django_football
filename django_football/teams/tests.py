from random import choice, randint

import factory
from django.test import TestCase

import cities
import nicknames

from .models import Team, TeamStats


class TeamFactory(factory.Factory):
    class Meta:
        model = Player

    # universe = universe
    city = factory.LazyAttribute(choice(cities))
    nickname = factory.LazyAttribute(choice(nicknames))
    human_control = False
    home_field_advantage = factory.LazyAttribute(randint(1,3))
    draft_position_order = get_draft_position_order()
    # coach = coaches
    # playbook = Playbook.objects.get(id=1)
    
    
class TeamTest(TestCase):
    def setUp(self):
        # league_teams = [TeamFactory() for team in xrange(8)]
        self.team1 = TeamFactory()
        
    def test_team_draft_order(self):
        print self.team1