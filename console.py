#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def split_arg(arg):
    """search arg to see if there are square brackets """
    has_curly_brackets = re.search(r"\{(.*?)\}", arg)
    """
    search arg to see if there are curly brackets using regex
    then transfer the result to the variable
    """
    has_sqr_brackets = re.search(r"\[(.*?)\]", arg)
    if has_curly_brackets is None:
        if has_sqr_brackets is None:
            """
            if there is no curly or sqr brackets,
            split the arg and remove the commas
            then convert it to a list
            """
            return [i.strip(",") for i in split(arg)]
        else:
            """
            if there are only sqr brackets, slice arg and remove
            the part before the sqr rackets
            and put it in lexer
            """
            lexer = split(arg[:has_sqr_brackets.span()[0]])
            """
            after slicing and extracting, split the exttracted
            and remove the commas then convert it to a list
            """
            splitted_list = [i.strip(",") for i in lexer]
            """
            now attach back the other sliced half with append
            """
            splitted_list.append(has_sqr_brackets.group())
            """
            close the function and return the returned_list
            back to sender
            """
            return splitted_list
    else:
        """
            else if there are only curly rackets,
            slice arg and remove
            the part before the curly brackets
            and put it in lexer. then run the flow as
            was done with sqr brackets
        """
        lexer = split(arg[:has_curly_brackets.span()[0]])
        """
            after slicing and extracting, split the exttracted
            and remove the commas then convert it to a list
        """
        splitted_list = [i.strip(",") for i in lexer]
        """
            now attach back the other sliced half with append
        """
        splitted_list.append(has_curly_brackets.group())
        """
            close the function and return the
            returned_list back to sender
        """
        return splitted_list

def split_me(arg):
    splitted_arg = shlex.split(arg)
    return splitted_arg


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter.

    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    """Do nothing upon receiving an empty line"""
    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    """handles unrecognized commands, its being called by the Cmd module"""
    def default(self, arg):
        """
        Default behavior for cmd module when input is invalid
        Default behavior for cmd module when input is invalid
        The methods are mapped to the corresponding input args
        For example, if the user enters "all,"
        it maps to the method do_all, and so on.
        """
        arg_to_dict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        """
        This checks if there's a dot (.) in the input, and if so,
        it splits the input into two parts (splited_arg_list)
        """
        match = re.search(r"\.", arg)
        if match is not None:
            """
            turn the splited parts into a list
            """
            splitted_arg_list = [arg[:match.span()[0]], arg[match.span()[1]:]]
            """
            here we use regex to find and extract content that is enclosed within
            parentheses in the second part of the splitted input.
            """
            match = re.search(r"\((.*?)\)", splitted_arg_list[1])
            if match is not None:
                """
                match.span() is a method of the match object returned by re.search,
                and it returns a tuple representing
                the start and end positions of the match.
                match.span()[0] extracts the start position of the match.
                ======
                splitted_arg_list[1][match.span()[0]] part of the expression is obtaining the content
                before the opening parenthesis.
                ======
                match.group()[1:-1] extracts a substring from the matched content,
                excluding the first and last characters.
                ======
                The purpose of this line is to extract two pieces of information:
                The content before the opening parenthesis.
                The content inside the parentheses, excluding the parentheses themselves.
                """
                command = [splitted_arg_list[1][:match.span()[0]], match.group()[1:-1]]
                """
                arg_to_dict.keys() returns a view of all the keys in the dictionary.
                """
                if command[0] in arg_to_dict.keys():
                    call = f"{splitted_arg_list[0]} {command[1]}"
                    return arg_to_dict[command[0]](call)
        print(f"*** Unknown syntax: {arg}")
        return False

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """
        EOF signal to exit the program.
        """
        print("")
        return True

    def do_create(self, arg):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        splitted_arg_list = split_arg(arg)
        if len(splitted_arg_list) == 0:
            print("** class name missing **")
        elif splitted_arg_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(splitted_arg_list[0])().id)
            storage.save()

    def do_show(self, arg):
        """
        Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        splitted_arg_list = split_arg(arg)
        all_obj_dict = storage.all()
        if len(splitted_arg_list) == 0:
            print("** class name missing **")
        elif splitted_arg_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(splitted_arg_list) == 1:
            print("** instance id missing **")
        elif f"{splitted_arg_list[0]}.{splitted_arg_list[1]}" not in all_obj_dict:
            print("** no instance found **")
        else:
            """Please check the provided sample data to understand
            what is happening
            """
            print(all_obj_dict["{}.{}".format(splitted_arg_list[0], splitted_arg_list[1])])

    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        splitted_arg_list = split_arg(arg)
        all_obj_dict = storage.all()
        if len(splitted_arg_list) == 0:
            print("** class name missing **")
        elif splitted_arg_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(splitted_arg_list) == 1:
            print("** instance id missing **")
        elif f"{splitted_arg_list[0]}.{splitted_arg_list[1]}" not in all_obj_dict.keys():
            print("** no instance found **")
        else:
            del all_obj_dict[f"{splitted_arg_list[0]}.{splitted_arg_list[1]}"]
            storage.save()

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        splitted_arg_list = split_arg(arg)
        if len(splitted_arg_list) > 0 and splitted_arg_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            my_obj_list = []
            for obj in storage.all().values():
                if len(splitted_arg_list) > 0 and splitted_arg_list[0] == obj.__class__.__name__:
                    my_obj_list.append(obj.__str__())
                elif len(splitted_arg_list) == 0:
                    my_obj_list.append(obj.__str__())
            print(my_obj_list)

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        splitted_arg_list = split_arg(arg)
        count = 0
        for obj in storage.all().values():
            if splitted_arg_list[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        splitted_arg_list = split_arg(arg)
        all_obj_dict = storage.all()

        if len(splitted_arg_list) == 0:
            print("** class name missing **")
            return False
        """Checks if the class name is provided and exists in the registered classes.
        """
        if splitted_arg_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        """
        Checks if the instance ID is provided and if an instance with that ID exists.
        """
        if len(splitted_arg_list) == 1:
            print("** instance id missing **")
            return False
        if f"{splitted_arg_list[0]}.{splitted_arg_list[1]}" not in all_obj_dict.keys():
            print("** no instance found **")
            return False
        """
        Checks if the attribute name is provided.
        """
        if len(splitted_arg_list) == 2:
            print("** attribute name missing **")
            return False
        """
        Checks if the value is provided when updating a specific attribute.
        """
        if len(splitted_arg_list) == 3:
            try:
                type(eval(splitted_arg_list[2])) != dict
            except NameError:
                print("** value missing **")
                return False
        """
        If all conditions are met, it proceeds to update the specified attribute
        of the instance with the given value.
        """
        if len(splitted_arg_list) == 4:
            obj = all_obj_dict["{}.{}".format(splitted_arg_list[0], splitted_arg_list[1])]
            if splitted_arg_list[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[splitted_arg_list[2]])
                obj.__dict__[splitted_arg_list[2]] = valtype(splitted_arg_list[3])
            else:
                obj.__dict__[splitted_arg_list[2]] = splitted_arg_list[3]
        elif type(eval(splitted_arg_list[2])) == dict:
            """checks to see if the value is a dictionary
            then iterates and updates every element provided
            """
            obj = all_obj_dict["{}.{}".format(splitted_arg_list[0], splitted_arg_list[1])]
            for my_key, val in eval(splitted_arg_list[2]).items():
                if (my_key in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[my_key]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[my_key])
                    obj.__dict__[my_key] = valtype(val)
                else:
                    obj.__dict__[my_key] = val
        storage.save()


if __name__ == "__main__":
    """
    HBNBCommand().cmdloop()
    the cmdloop() comes with the Cmd base class used to create 
    our HBNBCommand class. it does not have to be created.
    it uses the prompt specified.
    """
    my_cmd = HBNBCommand()
    my_cmd.cmdloop()
