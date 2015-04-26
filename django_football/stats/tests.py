from django.test import TestCase

from .utils import calculate_win_percentage

class TestUpdateStats(TestCase):
    def test_calculate_win_percentage(self):
        self.assertEquals(calculate_win_percentage(8,2,0), .8)
        self.assertEquals(calculate_win_percentage(6,3,1), .65)
        self.assertEquals(calculate_win_percentage(6,0,0), 1)
        self.assertEquals(calculate_win_percentage(0,13,0), 0)
