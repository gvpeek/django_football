from django.test import TestCase

import python_football

from core.models import Universe
from teams.models import City, Team
from people.models import Coach

class TeamTest(TestCase):
    def SetUp(self):
        universe = Universe.objects.create(name='Test')

        city = City.objects.create(name = 'Pascagoula',
                                   state = 'AZ',
                                   pro = True,
                                   semipro = True,
                                   amateur = False,
                                   region = 2,
                                   division = 4)
                                   
        coach = Coach.objects.create(universe = universe,
                                     first_name = 'Jimbo',
                                     last_name = 'Jones',
                                     skill = 80,
                                     play_probabilities = '',
                                     fg_dist_probabilities = '')
                                     
        playbook = Playbook(name='Basic',
                            plays=json.dumps(pickle.dumps(python_football.new_playbook())))
        
        Team.objects.create(universe = universe,
                            city = city,
                            nickname = 'Flotsam',
                            coach = coach,
                            playbook = playbook,
                            primary_color  = (000,333,666),
                            secondary_color = (123,123,123))
                            
    def test_team_app(self):
        print 'Testing app...'