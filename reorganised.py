import types
from dataclasses import dataclass
from typing import Callable, Any


class RecordMeta(type):
    """
    Defines a field with a label and preconditions
    """
    def __new__(cls, class_name, bases=None, dict=None):
        new_attr = dict.copy()
        for key, value in dict.items():
            if not key.startswith("__"):
                print(value)
                new_attr["__" + key + "__field"] = value
                new_attr[key] = property(cls.make_fget(key), cls.make_fset(key))
            else:
                new_attr[key] = value
        return super(RecordMeta, cls).__new__(cls, class_name, bases, new_attr)

    def make_fget(key):
        """
        Defines a field with a label and preconditions
        """
        def fget(self):
            return getattr(self, "__%s" % key)

        return fget

    def make_fset(key):
        """
        Defines a field with a label and preconditions
        """
        def fset(self, value):
            if hasattr(self, key):
                raise AttributeError("Attribute %s is readonly, cannot be set" % (key))
            setattr(self, "__" + key, value)
        return fset

    def __call__(self, *args, **kwargs):
        """This method is called when the constructor of the new class
        is to be used to create an object

        Parameters
        ----------
        args : tuple
            Position only arguments of the new class
        kwargs : dict
            Keyward only arguments of the new class

        """
        list_attr = [x for x in dir(self) if not x.startswith('_')]
        if len(list_attr) > len(kwargs):
            raise TypeError('Missing attribute')
        if len(list_attr) < len(kwargs):
            raise TypeError('More attributes provided')
        for key, value in kwargs.items():
            get_precondition = getattr(self, "__" + key + "__field").precondition
            if get_precondition is not None:
                if not get_precondition(value):
                    raise TypeError('Precondition for ' + key + ' has been violated.')
            # if isinstance(value, type):
            # self.make_fset()

        return super().__call__(*args, **kwargs)

    def __repr__(self):
        # prettify the printing of objects
        """
        This method prettifies the printing of objects.
        """
        val = str(self.__name__) + "(\n"
        for k, v in self.__dict__.items():
            if k.endswith("__field"):
                val += "  # " + str(v.label) + "\n  "
                is_string = False
                placeholder = k[0:-7]
                label = placeholder.split('__')[1]
                for y, z in self.__annotations__.items():
                    if y == label:
                        if str(z) == "<class 'str'>":
                            is_string = True
                            break
                if is_string:
                    val += str(label) + "='{" + placeholder + "}'\n"
                else:
                    val += str(label) + "={" + placeholder + "}\n"
        val += ")"
        return val


@dataclass
class Field:
    """
    Defines a field with a label and preconditions
    """
    label: str
    precondition: Callable[[Any], bool] = None

class Record(metaclass=RecordMeta):

    """
     A simple record object
    """
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        """
        This method overrides the string method and returns a prettified object.
        """
        dict = self.__dict__
        pretty_object = str(self.__class__)
        return pretty_object.format(**dict)


class Named(Record):
    """
    A base class for things with names
    """
    name: str = Field(label="The name")


class Animal(Named):
    """
    An animal
    """
    habitat: str = Field(label="The habitat", precondition=lambda x: x in ["air", "land", "water"])
    weight: float = Field(label="The animals weight (kg)", precondition=lambda x: 0 <= x)


class Dog(Animal):
    """
    A type of animal
    """
    bark: str = Field(label="Sound of bark")


class Person(Record):
    """
    A simple person record
    """
    name: str = Field(label="The name")
    age: int = Field(label="The person's age", precondition=lambda x: 0 <= x <= 150)
    income: float = Field(label="The person's income", precondition=lambda x: 0 <= x)


# james = Person(name="JAMES", age=150, income=332)
# print(str(james))
# # james.age = 2
# # print(james.age)
