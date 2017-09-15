from unittest import TestCase
from retro_route_puzzle import RetroRoutePuzzle

class TestRetroRoutePuzzle(TestCase):

    def test__load_map_from_file_wrong(self):
        """deve fallire se sbaglio il nome del file"""
        map_file_name = 'data.json22'
        self.assertRaises(Exception, RetroRoutePuzzle(map_file_name))


    def test__load_map_from_file_ok(self):
        """devo ottenere un'istanza di RetroRoutePuzzle"""
        map_file_name = 'data.json'
        rrp = RetroRoutePuzzle(map_file_name)
        assert isinstance(rrp, RetroRoutePuzzle)


    def test_navigate_and_collect_fail1(self):
        """ERROR:retro_route_puzzle:Cannot run algorithm on map. The map is None"""
        map_file_name = 'data2.json'
        rrp = RetroRoutePuzzle(map_file_name)
        self.assertEqual(False, rrp.navigate_and_collect(1, []))


    def test_navigate_and_collect_fail2(self):
        """ERROR:retro_route_puzzle:Cannot run algorithm on map. No objects to collects"""
        map_file_name = 'data.json'
        rrp = RetroRoutePuzzle(map_file_name)
        self.assertEqual(False, rrp.navigate_and_collect(1, []))

    def test_navigate_and_collect_fail3(self):
        """ERROR:retro_route_puzzle:Cannot run algorithm on map. The start room ID is not valid"""
        map_file_name = 'data.json'
        rrp = RetroRoutePuzzle(map_file_name)
        self.assertEqual(False, rrp.navigate_and_collect(-999, []))

    def test_navigate_and_collect_ok(self):
        map_file_name = 'data.json'
        oc = ['Knife', 'Potted Plant', 'Pillow']
        rrp = RetroRoutePuzzle(map_file_name)
        self.assertEqual(None, rrp.navigate_and_collect(1, oc))