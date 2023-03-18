# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/implementation/05_mocking_objects.ipynb.

# %% auto 0
__all__ = ['get_public_names', 'get_public_attributes', 'Mock']

# %% ../../nbs/implementation/05_mocking_objects.ipynb 2
from .functions import FunctionMock

from fastcore.basics import patch_to

# %% ../../nbs/implementation/05_mocking_objects.ipynb 9
from typing import Protocol

# %% ../../nbs/implementation/05_mocking_objects.ipynb 14
def _is_public_name(name: str):
    "Returns whether or not a (member) name is public"
    return not name.startswith('_')

def get_public_names(protocol: type) -> list[str]:
    "Returns all names that are considered public from the given class"
    names = [name for name in dir(protocol) if _is_public_name(name)]
    return names

# %% ../../nbs/implementation/05_mocking_objects.ipynb 20
def get_public_attributes(protocol: type(Protocol)) -> list[str]:
    "Return a list of all attributes of the given protocol that are considered public."
    attributes =  [name for name in protocol.__annotations__.keys() if _is_public_name(name)]
    return attributes

# %% ../../nbs/implementation/05_mocking_objects.ipynb 34
class Mock:
    def __init__(self, protocol: type(Protocol)):
        self._protocol = protocol
        self._init_function_mocks(self._protocol)
        
    def _init_function_mocks(self, protocol: type(Protocol)):
        public_names = get_public_names(protocol)
        self._function_mocks = {
            name: FunctionMock(getattr(protocol, name))
            for name in public_names
        }
    
    def __str__(self):
        return f'Mock[{self._protocol.__name__}]'
    
    def __repr__(self): return str(self)

# %% ../../nbs/implementation/05_mocking_objects.ipynb 37
@patch_to(Mock)
def __getattr__(self, name: str) -> FunctionMock:
    if name not in self._function_mocks:
        raise AttributeError(f"Name {name} not found in {self}")
        
    return self._function_mocks[name]
