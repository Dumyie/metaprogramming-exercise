import types
from dataclasses import dataclass
from typing import Callable, Any


class RecordMeta(type):
    def __new__(cls, class_name, bases=None, dict=None):
        new_attr = dict.copy()
        for key, value in dict.items():
            if not key.startswith("__"):
                print("key " + str(key) + " value:" + str(value))
                new_attr["__" + key] = True
                if value is None:
                    raise TypeError("argument is not defined" + str(key))
                elif key == '__str__':
                    cls.show(cls, class_name, dict)
                else:
                    pass

        return super(RecordMeta, cls).__new__(cls, class_name, bases, new_attr)
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
    # def __repr__(self):
    #     # prettify the printing of objects
    #     val = str(self.__name__) + "(\n"
    #     for k in dir(self):
    #         if not k.startswith("_"):
    #             val += "  # " + str(getattr(self, k).label) + "\n  "
    #             is_string = False
    #             for y, z in self.__annotations__.items():
    #                 if y == k:
    #                     if str(z) == "<class 'str'>":
    #                         is_string = True
    #                         break
    #             if is_string:
    #                 val += str(k) + "='{" + k + "}'\n"
    #             else:
    #                 val += str(k) + "={" + k + "}\n"
    #     val += ")"
    #     return val


@dataclass
class Field:
    """
    Defines a field with a label and preconditions
    """
    label: str
    precondition: Callable[[Any], bool] = None


class Record(metaclass=RecordMeta):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            list_attr = [x for x in self.__dir__() if not x.startswith('_')]
            newdict = self.__annotations__
            print(newdict, kwargs, list_attr, len(list_attr))
            if len(list_attr) < len(kwargs):
                raise TypeError("Extra argument passed")
            if len(list_attr) > len(kwargs):
                raise TypeError("missing argument")
            # if newdict[key] != type(value):
            #     raise TypeError("Incorrect value type. Expected: " + str(newdict[key]) + " got: " + str(type(value)))
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


class Person(Record):
    """
    A simple person record
    """
    name: str = Field(label="The name")
    age: int = Field(label="The person's age", precondition=lambda x: 0 <= x <= 150)
    income: float = Field(label="The person's income", precondition=lambda x: 0 <= x)
