import types
from dataclasses import dataclass
from typing import Callable, Any


class RecordMeta(type):
    def __new__(cls, class_name, bases=None, dict=None):
        new_attr = dict.copy()
        # x = super().__new__(cls, class_name, bases, dict)
        print(dict)
        for key, value in dict.items():
            if not key.startswith("__"):
                # print("key " + str(key) + " value:" + str(value))
                new_attr["__" + key] = True
                if value is None:
                    raise TypeError("argument is not defined" + str(key))
                elif key == '__str__':
                    cls.show(cls, class_name, dict)
                else:
                    if isinstance(value, type):
                        value = cls.getter_setter_gen(key, value)
                    new_attr[key] = value
        # new_dct = {}
        # for key, value in cls.__dict__.items():
        #     if isinstance(value, type):
        #         value = cls.getter_setter_gen(key, value)
        #     new_attr[key] = value
        # Creates a new class, using the modified dictionary as the class dict:
        # return type(cls)(cls.__name__, cls.__bases__, new_attr)
        return super(RecordMeta, cls).__new__(cls, class_name, bases, new_attr)

    def getter_setter_gen(name, type_):
        def getter(self):
            return getattr(self, "__" + name)

        def setter(self, value):
            if not isinstance(value, type_):
                raise TypeError(f"{name} attribute must be set to an instance of {type_}")
            setattr(self, "__" + name, value)

        return property(getter, setter)
    # def __init__(cls, name, bases, dct):
    #     print(cls.__dir__,name,bases,dct)
    #     for key, value in dct.items():
    #         list_attr = [x for x in cls.__dir__ if not x.startswith('_')]
    #         newdict = cls.__annotations__
    #         print(newdict, list_attr, len(list_attr))
    #         if len(list_attr) < len(kwargs):
    #             raise TypeError("Extra argument passed")
    #         if len(list_attr) > len(kwargs):
    #             raise TypeError("missing argument")
    #         if newdict[key] != type(value):
    #             raise TypeError("Incorrect value type. Expected: " + str(newdict[key]) + " got: " + str(type(value)))

    # def __repr__(self):
    #     # prettify the printing of objects
    #     val = str(self.__name__) + "(\n"
    #     attributes = [x for x in dir(self) if not x.startswith("_")]
    #     attributes = [x for x in dir(self) if not x.startswith("_")]
    #     # print(attributes,dir(self),self.__conf__)
    #     for k in attributes:
    #         val += "  # " + str(getattr(self, k).label) + "\n  "
    #         is_string = False
    #         for y, z in self.__annotations__.items():
    #             if y == k:
    #                 if str(z) == "<class 'str'>":
    #                     is_string = True
    #                     break
    #         if is_string:
    #             val += str(k) + "='{" + k + "}'\n"
    #         else:
    #             val += str(k) + "={" + k + "}\n"
    #             # print(k, getattr(self, k))
    #
    #     val += ")"
    #     return val

    def __repr__(self):
        # prettify the printing of objects
        val = str(self.__name__) + "(\n"
        for k, v in self.__dict__.items():
            if not k.startswith("_"):
                val += "  # " + str(v.label) + "\n  "
                is_string = False
                for y, z in self.__annotations__.items():
                    if y == k:
                        if str(z) == "<class 'str'>":
                            is_string = True
                            break
                if is_string:
                    val += str(k) + "='{" + k + "}'\n"
                else:
                    val += str(k) + "={" + k + "}\n"
                # print(k, getattr(self, k))

        val += ")"
        return val
@dataclass
class Field:
    """
    Defines a field with a label and preconditions
    """
    label: str
    precondition: Callable[[Any], bool] = None


# def auto_attr_check(args):
#     pass


# @auto_attr_check
class Record(metaclass=RecordMeta):
    def __init__(self, **kwargs):
        list_attr = [x for x in self.__dir__() if not x.startswith('_')]
        newdict = self.__annotations__
        # print(newdict, kwargs, list_attr, len(list_attr))
        if len(list_attr) < len(kwargs):
            raise TypeError("Extra argument passed")
        if len(list_attr) > len(kwargs):
            raise TypeError("missing argument")
        for key, value in kwargs.items():
            print('type', getattr(self,key),type(getattr(self,key)))
            # if newdict[key] != type(value):
            #     raise TypeError("Incorrect value type. Expected: " + str(newdict[key]) + " got: " + str(type(value)))
            # if isinstance(value, type):
            #     print(value,type,"yesssss")
            precond = getattr(self, key).precondition
            if precond is not None:
                precond_status = getattr(self, key).precondition(value)
                if not precond_status:
                    raise TypeError("Precondition invalid")

            setattr(self, key, value)

    def __str__(self):
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


james = Person(name="JAMES", age=100, income=332)
# james = Dog(name="Stan", habitat="land", weight=45, bark="ARF",test="test")
james.age = 2
print(james.age)
