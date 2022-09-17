# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_validators.ipynb.

# %% auto 0
__all__ = ['ArgumentValidator', 'ArgumentFunctionValidator']

# %% ../nbs/01_validators.ipynb 1
from typing import Protocol, Any, runtime_checkable
from .core import AnyCallable

# %% ../nbs/01_validators.ipynb 7
@runtime_checkable
class ArgumentValidator(Protocol):
    "Interface for all argument validators"
    def is_valid(self, argument: Any) -> bool:
        ...

# %% ../nbs/01_validators.ipynb 9
class ArgumentFunctionValidator:
    "Validate an argument by evaluating an arbitrary function"
    def __init__(self, func: AnyCallable[bool]):
        self._func = func
        
    def is_valid(self, argument: Any) -> bool:
        return self._func(argument)
    
assert isinstance(ArgumentFunctionValidator, ArgumentFunctionValidator)
