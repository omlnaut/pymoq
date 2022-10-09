# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/04_mocking.functions.ipynb.

# %% auto 0
__all__ = ['is_class_method', 'add_self_parameter', 'FunctionMock', 'Setup']

# %% ../../nbs/04_mocking.functions.ipynb 2
import inspect
from typing import Any

from ..core import AnyCallable
from ..argument_validators import ArgumentFunctionValidator
from ..signature_validators import SignatureValidator, signature_validator_from_arguments
from ..return_value_generators import ReturnValueGenerator

from fastcore.basics import patch_to

# %% ../../nbs/04_mocking.functions.ipynb 18
def is_class_method(func: AnyCallable) -> bool:
    "Returns true if the given function has a parameter called 'self'"
    signature = inspect.signature(func)
    return 'self' in signature.parameters

# %% ../../nbs/04_mocking.functions.ipynb 20
def add_self_parameter(args: tuple[Any]) -> list[Any]:
    return (None,) + args

# %% ../../nbs/04_mocking.functions.ipynb 22
class FunctionMock:
    "Mocks a function object based on its signature"
    def __init__(self, func: AnyCallable):
        self._func = func
        self._signature = inspect.signature(self._func)
        self._argument_names = list(self._signature.parameters.keys())
        self._setups = []
        
        self._is_class_method = is_class_method(self._func)
        
    def arguments_valid(self, *args, **kwargs) -> None:
        "Given an arbitrary argument list (both positional and keyword arguments), returns True if the mocked function could be called with those arguments"
        self._signature.bind(*args, **kwargs)
        return True

# %% ../../nbs/04_mocking.functions.ipynb 38
class Setup:
    "This class bundles a signature validator with a call-result-action"
    def __init__(self, signature_validator: SignatureValidator):
        self._signature_validator = signature_validator
        
    def is_valid(self, *args, **kwargs) -> bool:
        "Uses the underlying `SignatureValidator` to determine if the argument list is valid"
        return self._signature_validator.is_valid(*args, **kwargs)
        
    def returns(self, return_value_generator: ReturnValueGenerator) -> None:
        "Set the `ReturnValueGenerator` to be called when this setup is successfully called"
        self._return_value_generator = return_value_generator
        
    def get_return_value(self, *args, **kwargs):
        "Calls the underlying `ReturnValueGenerator` the get the return value for the exact argument list"
        return self._return_value_generator(*args, **kwargs)

# %% ../../nbs/04_mocking.functions.ipynb 40
@patch_to(FunctionMock)
def setup(self, *args, **kwargs):
    # todo: actually implement this
    sig = signature_validator_from_arguments(self._argument_names, *args, **kwargs)
    self._setups.append(Setup(sig))
    
    return self._setups[-1]

# %% ../../nbs/04_mocking.functions.ipynb 51
@patch_to(FunctionMock)
def fill_up_arg_list(self, args: list[Any], kwargs: dict[str, Any]) -> dict[str, Any]:
    parameters = list(self._signature.parameters.items())
    names = list(map(lambda p: p[0], parameters))
    n_positional = len(args)
    for name,param in parameters[n_positional:]:
        if name in kwargs: continue
        kwargs[name] = param.default
        
    return kwargs

# %% ../../nbs/04_mocking.functions.ipynb 59
@patch_to(FunctionMock)
def __call__(self, *args, **kwargs):
    if self._is_class_method:
        args = add_self_parameter(args)
    
    self.arguments_valid(*args, **kwargs)
        
    kwargs = self.fill_up_arg_list(args, kwargs)
    
    for setup in reversed(self._setups):
        if setup.is_valid(*args, **kwargs):
            return_value = setup.get_return_value(*args, **kwargs)
            return return_value
