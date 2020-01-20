import unittest
import datetime
import copy
from unittest import mock
from model.project import project
from model.innerList import innerList

# project.nameを書き換えておくことでテスト用のDBを利用する
@mock.patch("model.project.name")
def test_mock(self, mock_project_name):
    mock_project_name.return_value = "test_innerList"

class test_innerList(unittest.TestCase):

    def setUp(self):
        self.i = innerList.build()
        self.i.attr["user_id"] = 1
        self.i.attr["product_name"] = "tofu"
        self.i.attr["lim"] = 20201011
        self.i.attr["amount"] = 1
        self.i.attr["whose"] = "me"
        self.i.attr["kind"] = "newseihin"
        innerList.migrate()
        self.i.save()

    def tearDown(self):
        innerList.db_cleaner

    def test_db_is_working(self):
        i = innerList.find(self.i.attr["id"])
        self.assertTrue(type(i) is innerList)
        self.assertTrue(i.attr["id"] == 1)

    # attrが正しい値を持っている
    def test_is_valid(self):
        self.assertTrue(self.i.is_valid())

    # attrが間違った値を持っているかをチェックする関数のテスト
    def test_is_valid_with_invarid_attrs(self):
        i_wrong = copy.deepcopy(self.i)
        i_wrong.attr["id"] = None # id must be None or a int
        self.assertTrue(i_wrong.is_valid())

        i_wrong = copy.deepcopy(self.i)
        i_wrong.attr["id"] = "hoge" # id must be None or a int
        self.assertFalse(i_wrong.is_valid())

        i_wrong = copy.deepcopy(self.i)
        i_wrong.attr["user_id"] = None # password must be a string
        self.assertFalse(i_wrong.is_valid())

        i_wrong = copy.deepcopy(self.i)
        i_wrong.attr["product_name"] = "myname" # name must be a sting
        self.assertTrue(i_wrong.is_valid())

        i_wrong = copy.deepcopy(self.i)
        i_wrong.attr["lim"] = 20201011 # password must be a string
        self.assertTrue(i_wrong.is_valid())

        i_wrong = copy.deepcopy(self.i)
        i_wrong.attr["amount"] = None # password must be a string
        self.assertFalse(i_wrong.is_valid())

        i_wrong = copy.deepcopy(self.i)
        i_wrong.attr["whose"] = "me" # password must be a string
        self.assertTrue(i_wrong.is_valid())

        i_wrong = copy.deepcopy(self.i)
        i_wrong.attr["kind"] = "kind" # password must be a string
        self.assertTrue(i_wrong.is_valid())

    def test_build(self):
        i = innerList.build()
        self.assertTrue(type(i) is innerList)

    def test_save_INSERT(self):
        i = innerList.build()
        i.attr["user_id"] = 1
        i.attr["product_name"] = "tofu"
        i.attr["lim"] = 20201011
        i.attr["amount"] = 1
        i.attr["whose"] = "me"
        i.attr["kind"] = "newseihin"
        result = i.save()
        self.assertTrue(type(result) is int)
        self.assertTrue(i.attr["id"] is not None)

    def test_save_UPDATE(self):
        i = innerList.build()
        i.attr["id"] = 1
        i.attr["user_id"] = 1
        i.attr["product_name"] = "tofu"
        i.attr["lim"] = 20201011
        i.attr["amount"] = 1
        i.attr["whose"] = "me"
        i.attr["kind"] = "newseihin"
        result = i.save()
        self.assertTrue(type(result) is int)
        self.assertTrue(i.attr["id"] is not None)

    def test_delete(self):
        i = innerList.build()
        i.attr["id"] = 1
        i.attr["user_id"] = 1
        i.attr["product_name"] = "tofu"
        i.attr["lim"] = 20201011
        i.attr["amount"] = 1
        i.attr["whose"] = "me"
        i.attr["kind"] = "newseihin"
        result = i.save()
        self.assertTrue(type(result) is int)
        self.assertTrue(i.attr["id"] is not None)

if __name__ == '__main__':
    # unittestを実行
    unittest.main()
