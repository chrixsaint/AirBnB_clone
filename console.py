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


def handle_arg_splitting(arg):
    """search arg to see if there are square brackets """
    has_sqr_brackets = re.search(r"\[(.*?)\]", arg)
    """
    search arg to see if there are curly brackets using regex
    then transfer the result to the variable
    """
    has_curly_brackets = re.search(r"\{(.*?)\}", arg)
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
            the part before the sqr brackets
            and put it in lexer
             """
            lexer = split(arg[:has_sqr_brackets.span()[0]])
            """
            after slicing and extracting, split the exttracted
            and remove the commas then convert it to a list
            """
            returned_list = [i.strip(",") for i in lexer]
            """
            now attach back the other sliced half with append
            """
            returned_list.append(has_sqr_brackets.group())
            """
            close the function and return the returned_list
            back to sender
            """
            return returned_list
    else:
        """
            else if there are only curly brackets,
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
        returned_list = [i.strip(",") for i in lexer]
        """
            now attach back the other sliced half with append
        """
        returned_list.append(has_curly_brackets.group())
        """
            close the function and return the
            returned_list back to sender
        """
        return returned_list


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

    """Do nothing upon receiving an empty line."""
    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    """handles unrecognized commands, its being called by the Cmd module"""
    def default(self, arg):
        """
        Default behavior for cmd module when input is invalid
        The methods are mapped to the corresponding input args
        For example, if the user enters "all,"
        it maps to the method do_all, and so on.
        """
        arg_to_dict = {
            "all": self.do_all,
            "count": self.do_count,
            "update": self.do_update,
            "show": self.do_show,
            "destroy": self.do_destroy
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
            splited_arg_list = [arg[:match.span()[0]], arg[match.span()[1]:]]
            """
            here we use regex to find and extract content that is enclosed within
            parentheses in the second part of the splitted input.
            """
            match = re.search(r"\((.*?)\)", splited_arg_list[1])
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
                command = [splited_arg_list[1][:match.span()[0]], match.group()[1:-1]]
                """
                arg_to_dict.keys() returns a view of all the keys in the dictionary.
                """
                if command[0] in arg_to_dict.keys():
                    call = "{} {}".format(splited_arg_list[0], command[1])
                    return arg_to_dict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """
        Quit command to exit the program.
        """
        return True

    def do_EOF(self, arg):
        """
        EOF signal to exit the program."
        Handle End-of-File (Ctrl+D).
        """
        print("")
        return True

    def do_create(self, arg):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        splited_arg_list = handle_arg_splitting(arg)
        if len(splited_arg_list) == 0:
            print("** class name missing **")
        elif splited_arg_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(splited_arg_list[0])().id)
            storage.save()

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a
        class instance of a given id.
        """
        splited_arg_list = handle_arg_splitting(arg)
        objdict = storage.all()
        if len(splited_arg_list) == 0:
            print("** class name missing **")
        elif splited_arg_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(splited_arg_list) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(splited_arg_list[0], splited_arg_list[1]) not in objdict:
            print("** no instance found **")
        else:
            print(objdict["{}.{}".format(splited_arg_list[0], splited_arg_list[1])])

    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        splited_arg_list = handle_arg_splitting(arg)
        objdict = storage.all()
        if len(splited_arg_list) == 0:
            print("** class name missing **")
        elif splited_arg_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(splited_arg_list) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(splited_arg_list[0], splited_arg_list[1]) not in objdict.keys():
            print("** no instance found **")
        else:
            del objdict["{}.{}".format(splited_arg_list[0], splited_arg_list[1])]
            storage.save()

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        splited_arg_list = handle_arg_splitting(arg)
        if len(splited_arg_list) > 0 and splited_arg_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(splited_arg_list) > 0 and splited_arg_list[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(splited_arg_list) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        splited_arg_list = handle_arg_splitting(arg)
        count = 0
        for obj in storage.all().values():
            if splited_arg_list[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        splited_arg_list = handle_arg_splitting(arg)
        objdict = storage.all()

        if len(splited_arg_list) == 0:
            print("** class name missing **")
            return False
        if splited_arg_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(splited_arg_list) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(splited_arg_list[0], splited_arg_list[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(splited_arg_list) == 2:
            print("** attribute name missing **")
            return False
        if len(splited_arg_list) == 3:
            try:
                type(eval(splited_arg_list[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(splited_arg_list) == 4:
            obj = objdict["{}.{}".format(splited_arg_list[0], splited_arg_list[1])]
            if splited_arg_list[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[splited_arg_list[2]])
                obj.__dict__[splited_arg_list[2]] = valtype(splited_arg_list[3])
            else:
                obj.__dict__[splited_arg_list[2]] = splited_arg_list[3]
        elif type(eval(splited_arg_list[2])) == dict:
            obj = objdict["{}.{}".format(splited_arg_list[0], splited_arg_list[1])]
            for k, v in eval(splited_arg_list[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    """
        HBNBCommand().cmdloop()
        the cmdloop() comes with the Cmd base class used to create 
        our HBNBCommand class. it does not have to be created.
        it uses the prompt specified.
    """
    curr_cmd = HBNBCommand()
    curr_cmd.cmdloop()
