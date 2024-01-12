#!/usr/bin/python3
"""Defines unittests for models/city.py.

Unittest classes:
    TestCity_instantiation
    TestCity_save
    TestCity_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.city import City


class TestCity_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the City class."""

    def test_no_args_instantiates(self):
        self.assertEqual(City, type(City()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(City(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(City().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(City().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(City().updated_at))

    def test_state_id_is_public_class_attribute(self):
        city1 = City()
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(city1))
        self.assertNotIn("state_id", city1.__dict__)

    def test_name_is_public_class_attribute(self):
        city1 = City()
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(city1))
        self.assertNotIn("name", city1.__dict__)

    def test_two_cities_unique_ids(self):
        city11 = City()
        city12 = City()
        self.assertNotEqual(city11.id, city12.id)

    def test_two_cities_different_created_at(self):
        city11 = City()
        sleep(0.05)
        city12 = City()
        self.assertLess(city11.created_at, city12.created_at)

    def test_two_cities_different_updated_at(self):
        city11 = City()
        sleep(0.05)
        city12 = City()
        self.assertLess(city11.updated_at, city12.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        city1 = City()
        city1.id = "123456"
        city1.created_at = city1.updated_at = dt
        city1str = city1.__str__()
        self.assertIn("[City] (123456)", city1str)
        self.assertIn("'id': '123456'", city1str)
        self.assertIn("'created_at': " + dt_repr, city1str)
        self.assertIn("'updated_at': " + dt_repr, city1str)

    def test_args_unused(self):
        city1 = City(None)
        self.assertNotIn(None, city1.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        city1 = City(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(city1.id, "345")
        self.assertEqual(city1.created_at, dt)
        self.assertEqual(city1.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)


class TestCity_save(unittest.TestCase):
    """Unittests for testing save method of the City class."""

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
        city1 = City()
        sleep(0.05)
        first_updated_at = city1.updated_at
        city1.save()
        self.assertLess(first_updated_at, city1.updated_at)

    def test_two_saves(self):
        city1 = City()
        sleep(0.05)
        first_updated_at = city1.updated_at
        city1.save()
        second_updated_at = city1.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        city1.save()
        self.assertLess(second_updated_at, city1.updated_at)

    def test_save_with_arg(self):
        city1 = City()
        with self.assertRaises(TypeError):
            city1.save(None)

    def test_save_updates_file(self):
        city1 = City()
        city1.save()
        city1id = "City." + city1.id
        with open("file.json", "r") as f:
            self.assertIn(city1id, f.read())


class TestCity_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the City class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(City().to_dict()))

    def test_to_dict_contains_added_attributes(self):
        city1 = City()
        city1.middle_name = "Holberton"
        city1.my_number = 98
        """
        Confirm that city1.middle_name is equal to "Holberton"
        """
        self.assertEqual("Holberton", city1.middle_name)
        self.assertIn("my_number", city1.to_dict())

    def test_that_dict_contains_the_correct_keys(self):
        city1 = City()
        self.assertIn("id", city1.to_dict())
        self.assertIn("created_at", city1.to_dict())
        self.assertIn("updated_at", city1.to_dict())
        self.assertIn("__class__", city1.to_dict())

    def test_blablabla(self):
        dt = datetime.today()
        city1 = City()
        city1.id = "123456"
        city1.created_at = city1.updated_at = dt
        to_dict = {
            'id': '123456',
            '__class__': 'City',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(city1.to_dict(), to_dict)

    def test_contrast_to_dict_dunder_dict(self):
        city1 = City()
        self.assertNotEqual(city1.to_dict(), city1.__dict__)

    def test_to_dict_datetime_attributes_are_strs(self):
        city1 = City()
        city1_dict = city1.to_dict()
        self.assertEqual(str, type(city1_dict["id"]))
        self.assertEqual(str, type(city1_dict["created_at"]))
        self.assertEqual(str, type(city1_dict["updated_at"]))

    def test_to_dict_with_arg(self):
        city1 = City()
        with self.assertRaises(TypeError):
            city1.to_dict(None)


if __name__ == "__main__":
    unittest.main()
