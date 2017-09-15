from unittest import TestCase
from retro_route_puzzle import RetroRoutePuzzle

class TestRetroRoutePuzzle(TestCase):
    def test__load_map_from_file(self):
        map_file_name = 'data.json22'
        retro_route_puzzle = RetroRoutePuzzle(map_file_name)

        self.fail()
