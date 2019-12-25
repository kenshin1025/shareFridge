import unittest
import datetime
import copy
from unittest import mock
from model.project import project
from model.family import family

# project.nameを書き換えておくことでテスト用のDBを利用する
@mock.patch("model.project.name")
def test_mock(self, mock_project_name):
    mock_project_name.return_value = "test_family"

class test_family(unittest.TestCase):

    def setUp(self):
        self.f = family.build()
        self.f.attr["name"] = "Hoge"
        self.f.attr["password"] = "hogehogefugafuga"
        family.migrate()
        self.f.save()

    def tearDown(self):
        family.db_cleaner

    def test_db_is_working(self):
        f = family.find(self.f.attr["id"])
        self.assertTrue(type(f) is family)
        self.assertTrue(f.attr["id"] == 1)

    # attrが正しい値を持っている
    def test_is_valid(self):
        self.assertTrue(self.f.is_valid())

    # attrが間違った値を持っているかをチェックする関数のテスト
    def test_is_valid_with_invarid_attrs(self):
        cb_wrong = copy.deepcopy(self.f)
        cb_wrong.attr["id"] = None # id must be None or a int
        self.assertTrue(cb_wrong.is_valid())

        cb_wrong = copy.deepcopy(self.f)
        cb_wrong.attr["id"] = "1" # id must be None or a int
        self.assertFalse(cb_wrong.is_valid())

        cb_wrong = copy.deepcopy(self.f)
        cb_wrong.attr["name"] = None # password must be a string
        self.assertFalse(cb_wrong.is_valid())

        cb_wrong = copy.deepcopy(self.f)
        cb_wrong.attr["name"] = 12345 # name must be a sting
        self.assertFalse(cb_wrong.is_valid())

        cb_wrong = copy.deepcopy(self.f)
        cb_wrong.attr["name"] = "myname" # name must be a sting
        self.assertTrue(cb_wrong.is_valid())

        cb_wrong = copy.deepcopy(self.f)
        cb_wrong.attr["password"] = None # password must be a string
        self.assertFalse(cb_wrong.is_valid())

        cb_wrong = copy.deepcopy(self.f)
        cb_wrong.attr["password"] = 12345 # password must be a string
        self.assertFalse(cb_wrong.is_valid())

        cb_wrong = copy.deepcopy(self.f)
        cb_wrong.attr["password"] = "paspas" # password must be a string
        self.assertTrue(cb_wrong.is_valid())

    def test_build(self):
        f = family.build()
        self.assertTrue(type(f) is family)

    def test_save_INSERT(self):
        f = family.build()
        f.attr["name"] = "HogeHuga"
        f.attr["password"] = "HogeHogeFugaFuga"
        result = f.save()
        self.assertTrue(type(result) is int)
        self.assertTrue(f.attr["id"] is not None)

    def test_save_UPDATE(self):
        f = family.build()
        f.attr["id"] = 1
        f.attr["name"] = "new_Hoge"
        f.attr["password"] = "new_HogeHogeFugaFuga"
        result = f.save()
        self.assertTrue(type(result) is int)
        self.assertTrue(f.attr["id"] is not None)

if __name__ == '__main__':
    # unittestを実行
    unittest.main()