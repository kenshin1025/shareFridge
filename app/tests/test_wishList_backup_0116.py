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
        self.w.attr["name"] = "豆腐"
        self.w.attr["quantity"] = 1
        self.w.attr["kind"] = "乳製品"
        self.w.attr["last_updated"] = datetime.datetime.now()
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
        w_wrong.attr["kind"] = 12345 # quantity must be a string
        self.assertFalse(w_wrong.is_valid())

        w_wrong = copy.deepcopy(self.w)
        w_wrong.attr["last_updated"] = None # last_updated must be a datetime
        self.assertFalse(w_wrong.is_valid())

    def test_build(self):
        w = wishList.build()
        self.assertTrue(type(w) is wishList)

    def test_name(self):
        fridge_id = 2
        name = "豆腐"

        w1 = wishList.build()
        w1.attr["fridge_id"] = fridge_id
        w1.attr["name"] = name
        w1.attr["quantity"] = 1
        w1.attr["kind"] = "乳製品"
        w1_id = w1.save()

        w2 = wishList.build()
        w2.attr["fridge_id"] = fridge_id
        w2.attr["name"] = name
        w2.attr["quantity"] = 2
        w2.attr["kind"] = "乳製品"
        w2_id = w2.save()
        w_list = wishList.name(fridge_id, name)
        self.assertEqual(len(w_list), 2)
        self.assertTrue(type(w_list[0]) is wishList)
        self.assertTrue(w_list[0].attr["quantity"] < w_list[1].attr["quantity"])

    def test_kind(self):
        fridge_id = 2
        kind = "肉"

        w1 = wishList.build()
        w1.attr["fridge_id"] = fridge_id
        w1.attr["name"] = "牛肉"
        w1.attr["quantity"] = 1
        w1.attr["kind"] = kind
        w1_id = w1.save()

        w2 = wishList.build()
        w2.attr["fridge_id"] = fridge_id
        w2.attr["name"] = "豚肉"
        w2.attr["quantity"] = 2
        w2.attr["kind"] = kind
        w2_id = w2.save()
        w_list = wishList.kind(fridge_id, kind)
        self.assertEqual(len(w_list), 2)
        self.assertTrue(type(w_list[0]) is wishList)
        self.assertTrue(w_list[0].attr["quantity"] < w_list[1].attr["quantity"])

if __name__ == '__main__':
    # unittestを実行
    unittest.main()
