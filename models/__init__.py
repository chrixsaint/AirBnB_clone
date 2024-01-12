#!/usr/bin/python3
"""__init__ magic method for models directory"""
from models.engine.file_storage import FileStorage

"""
creating an instance of the filestorage to be used
for our storage.
"""
storage = FileStorage()
"""
 reload Deserializes back to dictionary from json format
"""
storage.reload()
