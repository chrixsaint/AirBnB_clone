#!/usr/bin/python3
"""This creates the BaseModel class."""
from uuid import uuid4
import models
from datetime import datetime


class BaseModel:
    """Represents the BaseModel of the HBnB project."""

    def __init__(self, *args, **kwargs):
        """creates a new instance of BaseModel.

        Args:
            **kwargs: Key value pair of attributes.
        """
        self.id = str(uuid4())
        self.updated_at = datetime.today()
        self.created_at = datetime.today()
        iso_date_format = "%Y-%m-%dT%H:%M:%S.%f"
        """
        e.g user = User(name="John", age=25, created_at="2022-01-01T12:00:00.000")
        """
        if len(kwargs) != 0:
            for k, v in kwargs.items():
                """
                handles datetime attributes
                """
                if k == "created_at" or k == "updated_at":
                    self.__dict__[k] = datetime.strptime(v, iso_date_format)
                else:
                    """handle the other items"""
                    self.__dict__[k] = v
        else:
            """
            e.g user = User()
            So, in short, the FileStorage class is designed
            to handle instances from various places
            in your code, and the new method gets called explicitly from
            the __init__ method of other classes, including BaseModel,
            when instances are created without existing data
            (i.e., when kwargs is empty).
            """
            models.storage.new(self)

    def save(self):
        """Update updated_at with the current datetime."""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """Return the dictionary of the BaseModel instance.

        Includes the key/value pair __class__ representing
        the class name of the object.
        """
        dict_copy = self.__dict__.copy()
        dict_copy["updated_at"] = self.updated_at.isoformat()
        dict_copy["created_at"] = self.created_at.isoformat()
        dict_copy["__class__"] = self.__class__.__name__
        return dict_copy

    def __str__(self):
        """Return the str representation of the BaseModel instance."""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
