#!/usr/bin/python3
"""Defines unittests for models/amenity.py.

Unittest classes:
    TestAmenity_instantiation
    TestAmenity_save
    TestAmenity_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity


class TestAmenity_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Amenity class."""

    def test_no_args_instantiates(self):
        self.assertEqual(Amenity, type(Amenity()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Amenity(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Amenity().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_name_is_public_class_attribute(self):
        pool = Amenity()
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", pool.__dict__)

    def test_two_amenities_unique_ids(self):
        tv = Amenity()
        heater = Amenity()
        self.assertNotEqual(tv.id, heater.id)

    def test_two_amenities_different_created_at(self):
        tv = Amenity()
        sleep(0.05)
        heater = Amenity()
        self.assertLess(tv.created_at, heater.created_at)

    def test_two_amenities_different_updated_at(self):
        tv = Amenity()
        sleep(0.05)
        heater = Amenity()
        self.assertLess(tv.updated_at, heater.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        pool = Amenity()
        pool.id = "123456"
        pool.created_at = pool.updated_at = dt
        amstr = pool.__str__()
        self.assertIn("[Amenity] (123456)", amstr)
        self.assertIn("'id': '123456'", amstr)
        self.assertIn("'created_at': " + dt_repr, amstr)
        self.assertIn("'updated_at': " + dt_repr, amstr)

    def test_args_unused(self):
        pool = Amenity(None)
        self.assertNotIn(None, pool.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """instantiation with kwargs test method"""
        dt = datetime.today()
        dt_iso = dt.isoformat()
        pool = Amenity(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(pool.id, "345")
        self.assertEqual(pool.created_at, dt)
        self.assertEqual(pool.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)


class TestAmenity_save(unittest.TestCase):
    """Unittests for testing save method of the Amenity class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        pool = Amenity()
        sleep(0.05)
        first_updated_at = pool.updated_at
        pool.save()
        self.assertLess(first_updated_at, pool.updated_at)

    def test_two_saves(self):
        pool = Amenity()
        sleep(0.05)
        first_updated_at = pool.updated_at
        pool.save()
        second_updated_at = pool.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        pool.save()
        self.assertLess(second_updated_at, pool.updated_at)

    def test_save_with_arg(self):
        pool = Amenity()
        with self.assertRaises(TypeError):
            pool.save(None)

    def test_save_updates_file(self):
        pool = Amenity()
        pool.save()
        amid = "Amenity." + pool.id
        with open("file.json", "r") as f:
            self.assertIn(amid, f.read())


class TestAmenity_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the Amenity class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Amenity().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        pool = Amenity()
        self.assertIn("id", pool.to_dict())
        self.assertIn("created_at", pool.to_dict())
        self.assertIn("updated_at", pool.to_dict())
        self.assertIn("__class__", pool.to_dict())

    def test_to_dict_contains_added_attributes(self):
        pool = Amenity()
        pool.middle_name = "Holberton"
        pool.my_number = 98
        self.assertEqual("Holberton", pool.middle_name)
        self.assertIn("my_number", pool.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        pool = Amenity()
        am_dict = pool.to_dict()
        self.assertEqual(str, type(am_dict["id"]))
        self.assertEqual(str, type(am_dict["created_at"]))
        self.assertEqual(str, type(am_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        pool = Amenity()
        pool.id = "123456"
        pool.created_at = pool.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'Amenity',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(pool.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        pool = Amenity()
        self.assertNotEqual(pool.to_dict(), pool.__dict__)

    def test_to_dict_with_arg(self):
        pool = Amenity()
        with self.assertRaises(TypeError):
            pool.to_dict(None)


if __name__ == "__main__":
    unittest.main()
