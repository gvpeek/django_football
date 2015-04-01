from django.test import TestCase
from tastypie.test import ResourceTestCase

from teams.models import Team

# Create your tests here.

class TeamResourceTest(ResourceTestCase):    
    def SetUp(self):
        super(TeamResourceTest, self).setUp()
    
    def test_team_api(self):
        print 'Running'
        
        