from typing import TypeVar, Type

T = TypeVar('T')


class Inner:
    def inner_func(self):
        return 1


class Outer:
    def __init__(self, cls):
        self.cls = cls

    def __dir__(self):
        return dir(self.cls)

    @classmethod
    def from_cls(cls,  other_cls: Type[T]) -> T:
        return cls(other_cls)


def public_members(l):
    return [el for el in l if not el.startswith('__')]


o = Outer(Inner).from_cls(Inner)

print(public_members(dir(o)))
