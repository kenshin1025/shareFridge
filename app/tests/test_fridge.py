import unittest
import datetime
import copy
from unittest import mock
from model.project import project
from model.fridge import fridge


@mock.patch("model.project.name")
def test_mock(self, mock_project_name):
        mock_project_name.return_value = "test_fridge"

class test_fridge(unittest.TestCase):
        def setUp(self):
                self.f = fridge.build()
                self.f.attr["famiry_id"] = 1
                fridge.migrate()
                self.f.save()
        
        def tearDown(self):
                fridge.db_cleaner

        def test_db_is_working(self):
                f = fridge.find(self.f.attr["id"])
                self.assertTrue(type(f) is fridge)
                self.assertTrue(f.attr["id"] == 1)

        def test_is_valid(self):
                self.assertTrue(self.f.is_valid())

        def test_is_valid_with_invarid_attrs(self):
                cb_wrong = copy.deepcopy(self.f)
                cb_wrong.attr["id"] = None # id must be None or a int
                self.assertTrue(cb_wrong.is_valid())


                cb_wrong = copy.deepcopy(self.f)
                cb_wrong.attr["id"] = "1" # id must be None or a int
                self.assertFalse(cb_wrong.is_valid())


                cb_wrong = copy.deepcopy(self.f)
                cb_wrong.attr["famiry_id"] = None # id must be None or a int
                self.assertFalse(cb_wrong.is_valid())


                cb_wrong = copy.deepcopy(self.f)
                cb_wrong.attr["famiry_id"] = "1" # id must be None or a int
                self.assertFalse(cb_wrong.is_valid())

        def test_build(self):
                f = fridge.build()
                self.assertTrue(type(f) is fridge)
        
        def test_save_INSERT(self):
                f = fridge.build()
                f.attr["id"] = 1
                f.attr["famiry_id"] = 1
                result = f.save()
                self.assertTrue(type(result) is int)
                self.assertTrue(f.attr["id"] is not None)

        def test_save_UPDATE(self):
                f = fridge.build()
                f.attr["id"] = 1
                f.attr["famiry_id"] = 2
                result = f.save()
                self.assertTrue(type(result) is int)
                self.assertTrue(f.attr["id"] is not None)

if __name__ == '__main__':
        unittest.main()
