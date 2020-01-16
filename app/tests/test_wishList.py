import unittest
import datetime
import copy
from unittest import mock
from model.project import project
from model.wishList import wishList

# project.nameを書き換えておくことでテスト用のDBを利用する
@mock.patch("model.project.name")
def test_mock(self, mock_project_name):
    mock_project_name.return_value = "test_wishList"

class test_wishList(unittest.TestCase):

    def setUp(self):
        self.w = wishList.build()
        self.w.attr["fridge_id"] = 1
        self.w.attr["name"] = "tofu"
        self.w.attr["quantity"] = 1
        self.w.attr["class"] = "newseihin"
        wishList.migrate()
        self.w.save()

    def tearDown(self):
        wishList.db_cleaner()

    def test_db_is_working(self):
        w = wishList.find(self.w.attr["id"])
        # findで帰ってきているのがidならDBに保存されている
        self.assertTrue(type(w) is wishList)
        # 最初だからidが1になる
        self.assertTrue(w.attr["id"] == 1)

    # attrが正しい値を持っている
    def test_is_valid(self):
        self.assertTrue(self.w.is_valid())

    # attrが間違った値を持っているかをチェックする関数のテスト
    def test_is_valid_with_invarid_attrs(self):
        w_wrong = copy.deepcopy(self.w)
        w_wrong.attr["id"] = None # id must be None or a int
        self.assertTrue(w_wrong.is_valid())

        w_wrong = copy.deepcopy(self.w)
        w_wrong.attr["id"] = "1" # id must be None or a int
        self.assertFalse(w_wrong.is_valid())

        w_wrong = copy.deepcopy(self.w)
        w_wrong.attr["fridge_id"] = None # fridge_id must be None or a int
        self.assertFalse(w_wrong.is_valid())

        w_wrong = copy.deepcopy(self.w)
        w_wrong.attr["name"] = 12345 # name must be a sting
        self.assertFalse(w_wrong.is_valid())

        w_wrong = copy.deepcopy(self.w)
        w_wrong.attr["quantity"] = None # quantity must be a int
        self.assertFalse(w_wrong.is_valid())

        w_wrong = copy.deepcopy(self.w)
        w_wrong.attr["class"] = 12345 # quantity must be a string
        self.assertFalse(w_wrong.is_valid())

        w_wrong = copy.deepcopy(self.w)
        w_wrong.attr["last_updated"] = None # last_updated must be a datetime
        self.assertFalse(w_wrong.is_valid())

    def test_build(self):
        w = wishList.build()
        self.assertTrue(type(w) is wishList)

    def test_save_INSERT(self):
        w = wishList.build()
        w.attr["fridge_id"] = 1
        w.attr["name"] = "tofu"
        w.attr["quantity"] = 1
        w.attr["class"] = "newseihin"
        result = w.save()
        self.assertTrue(type(result) is int)
        self.assertTrue(w.attr["id"] is not None)

    def test_save_UPDATE(self):
        w = wishList.build()
        w.attr["id"] = 1
        w.attr["fridge_id"] = 1
        w.attr["name"] = "new_tofu"
        w.attr["quantity"] = 1
        w.attr["class"] = "newseihin"
        result = w.save()
        self.assertTrue(type(result) is int)
        self.assertTrue(w.attr["id"] is not None)

    def test_move(self):
        w = wishList.move(1)
        # moveで帰ってきているのがidならDBに保存されている
        self.assertTrue(type(w) is wishList)


if __name__ == '__main__':
    # unittestを実行
    unittest.main()
