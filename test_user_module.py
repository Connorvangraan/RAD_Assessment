from unittest import TestCase
import pathlib as pl
from user_module import User

class Test(TestCase):
    def test_create_user_database(self):
        if not pl.Path("data/users.sqlite").resolve().is_file():
            raise AssertionError("File does not exist: %s" % str("data/users.sqlite"))




class TestUser(TestCase):
    @classmethod
    def setUp(self):
        self.user = User()

    def test_list_users(self):
        self.assertIsInstance(self.user.list_users(), dict, "No dictionary received")
        self.assertGreaterEqual(len(self.user.list_users().keys()), 1, "No entries in dictionary")

    def test_get_user(self):
        retrieved_data = self.user.get_user("fn@gmail.com heavyweight_champ")
        real_data = {'id': 1, 'fname': 'Francis', 'lname': 'Ngannou', 'phone_num': '024898114527', 'email': 'fn@gmail.com', 'password': 'heavyweight_champ'}
        self.assertDictEqual(real_data, retrieved_data, "Retrieved data does not match")

    def test_set_user(self):
        stored_data = self.user.get_user("test@email.com fake_person")

        if stored_data.get("USER NOT FOUND", 1) == 0:
            self.user.set_user("Test", "Johnson", "012345678910", "test@email.com", "fake_person")
            stored_data = self.user.get_user("test@email.com fake_person")

        real_data = {'id': stored_data['id'], 'fname': 'Test', 'lname': 'Johnson', 'phone_num': '12345678910', 'email': 'test@email.com', 'password': 'fake_person'}
        self.assertDictEqual(real_data, stored_data, "Data not stored")

    def test_update_user(self):
        stored_data = self.user.get_user("test2@email.com faker_person")

        if stored_data.get("USER NOT FOUND", 1) == 0:
            self.user.set_user("Tester", "Steve", "01239967910", "test2@email.com", "faker_person")
            print(self.user.get_user("test2@email.com faker_person"))

        self.user.update_user("test2@email.com faker_person", {"fname":"Jarvis_test", 'lname': 'Jackson', 'phone_num': '01235558910'})

        new_data = self.user.get_user("test2@email.com faker_person")
        print(self.user.get_user("test2@email.com faker_person"))
        real_data = {'id': new_data['id'], "fname":"Jarvis_test", 'lname': 'Jackson', 'phone_num': '01235558910', 'email': 'test2@email.com', 'password': 'faker_person'}

        self.assertDictEqual(real_data, new_data, "Update failed")

    def test_delete_user(self):
        stored_data = self.user.get_user("test@email.com fake_person")

        if stored_data.get("USER NOT FOUND", 1) == 0:
            self.user.set_user("Test", "Johnson", "012345678910", "test@email.com", "fake_person")

        self.user.delete_user("test@email.com fake_person")
        self.assertEqual(self.user.get_user("test@email.com fake_person").get("USER NOT FOUND",1), 0, "Station failed to delete")
