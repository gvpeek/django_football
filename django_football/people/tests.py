from django.test import TestCase

from .views import get_min_max_ratings, _check_rating_range_stub
# Create your tests here.

class RatingRangeTest(TestCase):
    def test_get_min_max_ratings(self):
        self.assertEqual(get_min_max_ratings(), [(14,(20,50)),
                                                 (18,(30,60)),
                                                 (22,(45,75)),
                                                 (99,(60,90))])
                                                 
    def test_check_rating_range_stub(self):
        self.assertEqual(_check_rating_range_stub(80, (45,75), ''), (75, ''))
        self.assertEqual(_check_rating_range_stub(75, (45,75), ''), (75, ''))
        self.assertEqual(_check_rating_range_stub(40, (45,75), ''), (40, 'R'))