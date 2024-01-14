#!/usr/bin/python3
"""Defines the FileStorage class."""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Represent an abstracted storage engine.

    Attributes:
        __file_path: The name of the file to save objects to.
        __objects: A dictionary of instantiated objects.
    """
    __objects = {}
    __file_path = "file.json"

    def all(self):
        """Return the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Set in __objects obj with key <obj_class_name>.id"""
        obj_cls_name = obj.__class__.__name__
        """save the "classname.id" to __objects, this reps the object in the dict"""
        FileStorage.__objects["{}.{}".format(obj_cls_name, obj.id)] = obj

    """Serialize __objects to the JSON file __file_path."""
    def save(self):
        """retrieve all available objects"""     
        avail_objs = FileStorage.__objects
        """
        loop through the objects and
        Serialize or convert available objs to the JSON
        file stored in __file_path.
        """
        obj_d = {obj: avail_objs[obj].to_dict() for obj in avail_objs.keys()}
        """write the objects into a file in json format"""     
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            json.dump(obj_d, f)

    def reload(self):
        """Deserialize the JSON file __file_path to __objects, if it exists."""
        try:
            with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
                obj_d = json.load(f)
                """
                It iterates over the values of the obj_d dictionary
                Each value represents a serialized object stored in the JSON file.
                """
                for item in obj_d.values():
                    """
                    retrieves the class name of the current serialized object
                    __class__ is the key used to store the class name of the object
                    I have provided a sample of some serialized objects for better understanding
                    {
                        "BaseModel.604fc043-6ba7-420e-b375-9ff4a54b10bf":
                        {
                            "id": "604fc043-6ba7-420e-b375-9ff4a54b10bf",
                             "created_at": "2024-01-11T10:39:56.747981",
                             "updated_at": "2024-01-11T10:39:56.749720",
                             "first_name": "Betty",
                             "__class__": "BaseModel"
                        },
                        "SecondModel.7804fc043-6ba7-420e-b375-9ff4a54b10bf":
                        {
                            "id": "604fc043-6ba7-420e-b375-9ff4a54b10bf",
                             "created_at": "2024-01-11T10:39:56.747981",
                             "updated_at": "2024-01-11T10:39:56.749720",
                             "first_name": "Betty",
                             "__class__": "SecondModel"
                        }
                    }
                    """
                    cls_name = item["__class__"]
                    """
                    delete the __class__ object, it is no longer needed
                    we would later pass the other items like id, created_at etc
                    into an instance that would be dynamically created
                    and we dont want classnameas part of the "**item" that would be passed
                    """
                    del item["__class__"]
                    """
                    with the retrieved classname an instance
                    can be dynamically created using the eval() function.
                    the **item is passed in as keyword args to the created instance.
                    my_new_instance = BaseModel(self, **item) this is
                    what hapened with the eval()
                    """
                    self.new(eval(cls_name)(**item))
        except FileNotFoundError:
            return
 