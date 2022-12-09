from unittest import TestCase
import pathlib as pl

from radio_module import Radio


class Test(TestCase):
    def test_create_radio_database(self):
        if not pl.Path("data/stations.sqlite").resolve().is_file():
            raise AssertionError("File does not exist: %s" % str("data/users.sqlite"))


class TestRadio(TestCase):
    @classmethod
    def setUpClass(self):
        self.radio = Radio()

    def test_list_stations(self):
        self.assertIsInstance(self.radio.list_stations(), dict, "No dictionary recieved")
        self.assertGreaterEqual(len(self.radio.list_stations().keys()), 1, "No entries in dictionary")

    def test_get_station(self):
        retrieved_data = self.radio.get_station("SKY.FM: Simply Soundtracks")
        real_data = {'id': 254, 'name': 'SKY.FM: Simply Soundtracks', 'link': ' http://www.sky.fm/mp3/soundtracks.pls'}
        self.assertDictEqual(real_data, retrieved_data, "Retrieved data does not match")

    def test_set_station(self):
        stored_data = self.radio.get_station("Test FM")
        print(stored_data)
        if stored_data == "STATION NOT FOUND":
            self.radio.set_station("Test FM", "www.testfm.com")
            stored_data = self.radio.get_station("Test FM")

        real_data = {'id': 521, 'name': 'Test FM', 'link': 'www.testfm.com'}
        self.assertDictEqual(real_data, stored_data)

    def test_update_station(self):
        old_data = self.radio.get_station("Test FM")
        if old_data == "STATION NOT FOUND":
            self.radio.set_station("Test FM", "www.testfm.com")

        self.radio.update_station("Test FM", "www.testfm.net", "Test FM Radio")
        new_data = self.radio.get_station("Test FM Radio")
        real_data = {'id': 521, 'name': 'Test FM Radio', 'link': 'www.testfm.net'}
        self.assertDictEqual(real_data, new_data, "Update failed")

    def test_delete_station(self):
        old_data = self.radio.get_station("Test FM")
        if old_data == "STATION NOT FOUND":
            self.radio.set_station("Test FM", "www.testfm.com")

        self.radio.delete_station("Test FM")
        self.assertEqual(self.radio.get_station("Test FM"), "STATION NOT FOUND", "Station failed to delete")