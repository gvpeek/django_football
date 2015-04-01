from django.test import TestCase
from django.db.models import F

from .models import Universe, Player
from .views import get_min_max_ratings, _check_rating_range_stub, age_players
# Create your tests here.

class PlayerTest(TestCase):
    def setUp(self):
        universe = Universe.objects.create(name='Test')
        
        Player.objects.create(universe=universe,
                      first_name='Smiley',
                      last_name='Wilson',
                      age = 11,
                      position = 'P',
                      constitution = 25,
                      retired = False,
                      apex_age = 29,
                      growth_rate = 4,
                      declination_rate = 5,
                      ratings = 30,
                      future_ratings = 40)
                      
        Player.objects.create(universe=universe,
                      first_name='Youngman',
                      last_name='Grand',
                      age = 17,
                      position = 'P',
                      constitution = 25,
                      retired = False,
                      apex_age = 29,
                      growth_rate = 4,
                      declination_rate = 5,
                      ratings = 27,
                      future_ratings = 29)
        
        Player.objects.create(universe=universe,
                      first_name='Frowny',
                      last_name='Scratch',
                      age = 35,
                      position = 'WR',
                      constitution = 25,
                      retired = False,
                      apex_age = 29,
                      growth_rate = 4,
                      declination_rate = 5,
                      ratings = 80,
                      future_ratings = 70)
                      
        Player.objects.create(universe=universe,
                      first_name='Old',
                      last_name='Bear',
                      age = 37,
                      position = 'OL',
                      constitution = 25,
                      retired = False,
                      apex_age = 29,
                      growth_rate = 4,
                      declination_rate = 5,
                      ratings = 60,
                      future_ratings = 55)
                                    
        Player.objects.create(universe=universe,
                      first_name='Wonder',
                      last_name='Man',
                      age = 24,
                      position = 'OL',
                      constitution = 25,
                      retired = False,
                      apex_age = 29,
                      growth_rate = 4,
                      declination_rate = 5,
                      ratings = 88,
                      future_ratings = 92)
                      
    def test_player_functions(self):
        universe = Universe.objects.get(name='Test')
        player = Player.objects.get(first_name='Smiley')
        self.assertEqual(player.age, 11)
        
        age_players(universe)
        player = Player.objects.get(first_name='Smiley')
        self.assertEqual(player.age, 12)
        self.assertEqual(player.ratings, 40)
        self.assertFalse(player.retired)
        
        player = Player.objects.get(first_name='Youngman')
        self.assertEqual(player.age, 18)
        self.assertEqual(player.ratings, 29)
        self.assertTrue(player.retired)
        
        player = Player.objects.get(first_name='Frowny')
        self.assertEqual(player.age, 36)
        self.assertEqual(player.ratings, 70)
        self.assertFalse(player.retired)
        
        player = Player.objects.get(first_name='Old')
        self.assertEqual(player.age, 38)
        self.assertEqual(player.ratings, 55)
        self.assertTrue(player.retired)

        player = Player.objects.get(first_name='Wonder')
        self.assertEqual(player.age, 25)
        self.assertEqual(player.ratings, 90)
        self.assertFalse(player.retired)

class RatingRangeTest(TestCase):
    def test_get_min_max_ratings(self):
        self.assertEqual(get_min_max_ratings(), [((11,14),(20,50)),
                                                 ((15,18),(30,60)),
                                                 ((19,22),(45,75)),
                                                 ((23,99),(60,90))])
                                                 
    def test_check_rating_range_stub(self):
        self.assertEqual(_check_rating_range_stub(80, (45,75), ''), (75, ''))
        self.assertEqual(_check_rating_range_stub(75, (45,75), ''), (75, ''))
        self.assertEqual(_check_rating_range_stub(40, (45,75), ''), (40, 'R'))