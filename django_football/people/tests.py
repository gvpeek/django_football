from math import floor
from random import choice, randint

import factory
from django.test import TestCase
from django.db.models import F

import names

from .models import Universe, Player
from .views import get_min_max_ratings, _check_rating_range_stub, age_players
# Create your tests here.


class PlayerFactory(factory.Factory):
    class Meta:
        model = Player
        
    age = 11
    retired = False
    first_name = factory.LazyAttribute(lambda a: names.first_name())
    last_name = factory.LazyAttribute(lambda a: names.last_name())
    position = factory.LazyAttribute(lambda a: choice(Player.POSITIONS)[0])
    constitution = factory.LazyAttribute(lambda a: randint(25,40))
    apex_age = factory.LazyAttribute(lambda a: (floor(((32 * 100) * pow(randint(5,100),-.5)) / 100) + 18))
    growth_rate = factory.LazyAttribute(lambda a: randint(1,4))
    declination_rate = factory.LazyAttribute(lambda a: randint(3,5))
    ratings = factory.LazyAttribute(lambda a: randint(25,40))


class PlayerTest(TestCase):
    def setUp(self):
        Universe.objects.create(name='Test')
        
        universe = Universe.objects.get(name='Test')
        
        self.player1 = PlayerFactory()
        self.player2 = PlayerFactory()
        
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
        
        print vars(self.player1)
        print vars(self.player2)

    def test_get_min_max_ratings(self):
        self.assertEqual(get_min_max_ratings(), [((11,14),(20,50)),
                                                 ((15,18),(30,60)),
                                                 ((19,22),(45,75)),
                                                 ((23,99),(60,90))])
                                                 
    def test_check_rating_range_stub(self):
        self.assertEqual(_check_rating_range_stub(80, (45,75), ''), (75, ''))
        self.assertEqual(_check_rating_range_stub(75, (45,75), ''), (75, ''))
        self.assertEqual(_check_rating_range_stub(40, (45,75), ''), (40, 'R'))
        
        
class DraftTest(TestCase):
    def test_determine_draft_order(self):
        pass