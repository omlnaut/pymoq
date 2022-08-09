from typing import TypeVar, Type

from inspect import signature
from typing import Any, List

from typing import Protocol

class IWeb(Protocol):
    def get(url: str) -> str:
        pass

def is_public(name: str) -> bool:
    return not name.startswith('_')

def get_public_attributes(cls : Any) -> List[str]:
    return list(filter(is_public, dir(cls)))


from typing import Callable
import sys


class FunctionMocker:
    def __init__(self, target_function: Callable[[Any], Any], top_level: str = ""):
        self.name = target_function.__name__
        self.target_signature = signature(target_function)
        self._error_prefix = f'{top_level}.' if top_level else ''

    def _validate_signature(self, *args, **kwargs):
        try:
            self.target_signature.bind(*args, **kwargs)
        except TypeError as e:
            ei = sys.exc_info()
            raise ei[0](TypeError(f'{self._error_prefix}{self.name}{self.target_signature}: {e}')).with_traceback(
                ei[2].tb_next.tb_next.tb_next) from None
            # raise ei[0], TypeError(f'{self._error_prefix}{self.name}{self.target_signature}: {e}'), ei[2].tb_next
            # raise TypeError(f'{self._error_prefix}{self.name}{self.target_signature}: {e}') from None

    def setup(self):
        pass

    def __call__(self, *args, **kwargs):
        self._validate_signature(*args, **kwargs)

        print('Correct signature, start pattern matching')

    def __str__(self):
        return f'Moq: {self.name}{self.target_signature}'

    def __repr__(self):
        return str(self)

T = TypeVar('T')
U = TypeVar('U')


class Moq:
    def __init__(self, cls):
        self.cls_name = cls.__name__
        self._extract_attributes(cls)

    @classmethod
    def from_class(cls, other_class: T) -> T:
        return cls(other_class)

    def _extract_attributes(self, cls):
        self.attribute_names = get_public_attributes(cls)
        self.moq_functions = {name: FunctionMocker(getattr(cls, name), self.cls_name)
                              for name in self.attribute_names}

    def __getattr__(self, name):
        if name not in self.moq_functions:
            raise AttributeError(f"No attribute with name '{name}' in class {self.cls_name}")

        return self.moq_functions[name]

    def __dir__(self):
        return dir(super()) + self.attribute_names


class Wrapper:
    def __init__(self, cls):
        t = TypeVar('t', bound=cls)
        self.object: t = Moq.from_class(cls)
        self.testi : IWeb = 1

    def setup(self, c: Callable[[str], int]):
        pass


m = Wrapper(IWeb).setup(lambda s: s.)
