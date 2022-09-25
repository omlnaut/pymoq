# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/04_mocking.functions.ipynb.

# %% auto 0
__all__ = ['FunctionMock', 'Setup']

# %% ../../nbs/04_mocking.functions.ipynb 1
import inspect
from ..core import AnyCallable
from ..signature_validators import SignatureValidator, signature_validator_from_arguments
from ..return_value_generators import ReturnValueGenerator
from fastcore.basics import patch_to

# %% ../../nbs/04_mocking.functions.ipynb 11
class FunctionMock:
    "Mocks a function object based on its signature"
    def __init__(self, func: AnyCallable):
        self._func = func
        self._signature = inspect.signature(self._func)
        self._setups = []
        
    def arguments_valid(self, *args, **kwargs) -> bool:
        "Given an arbitrary argument list (both positional and keyword arguments), returns True if the mocked function could be called with those arguments"
        try:
            self._signature.bind(*args, **kwargs)
            return True
        except:
            return False

# %% ../../nbs/04_mocking.functions.ipynb 21
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