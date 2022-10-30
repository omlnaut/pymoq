# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/02_signature_validators.ipynb.

# %% auto 0
__all__ = ['VERBOSE', 'SignatureValidator', 'signature_validator_from_arguments']

# %% ../nbs/02_signature_validators.ipynb 2
from .argument_validators import ArgumentValidator, ArgumentFunctionValidator, argument_validator_from_argument 
from typing import Any
from fastcore.basics import patch_to
from itertools import chain

# %% ../nbs/02_signature_validators.ipynb 6
class SignatureValidator:
    "This class holds a list of argument validators and can evaluate a list of arguments against those validators"
    def __init__(self, argument_validators: list[ArgumentValidator]):
        self.argument_validators = argument_validators
        self._named_validators = {validator.name: validator
                                  for validator in self.argument_validators}
        
        self._positional_validators = {validator.position: validator
                                      for validator in self.argument_validators}
        
        names = [validator.name for validator in self.argument_validators]
        if len(names) != len(set(names)):
            raise ValueError(f"List of argument validators contains duplicate names: {names}")
            
        positions = [validator.position for validator in self.argument_validators]
        if len(positions) != len(set(positions)):
            raise ValueError(f"List of argument validators contains duplicate positions: {positions}")
        
    def is_valid(self, *args: list[Any], **kwargs: dict[str, Any]) -> bool:
        if len(args) > len(self.argument_validators): return False
    
        # positional arguments
        for position, value in enumerate(args):
            if not position in self._positional_validators.keys(): return False
            
            if not self._positional_validators[position].is_valid(value): return False
        
        # named arguments
        for name,value in kwargs.items():
            if name not in self._named_validators: return False
        
            if not self._named_validators[name].is_valid(value): return False
        
        return True
    
    def __str__(self) -> str:
        validator_string = '\n\t'.join(map(str, self._positional_validators.values())) + '\n\t'.join(map(str, self._named_validators.values()))
        return 'SignatureValidator:\n\t' + \
    'Positional:\n\t\t' + '\n\t\t'.join(map(str, self._positional_validators.values())) + \
    '\n\tNamed\n\t\t' + '\n\t\t'.join(map(str, self._named_validators.values()))
    
    def __repr__(self): return str(self)

# %% ../nbs/02_signature_validators.ipynb 20
VERBOSE = False

def signature_validator_from_arguments(argument_names: list[str], *args, **kwargs) -> SignatureValidator:
    "Construct a `SignatureValidator` by smartly constructing `ArgumentValidators` when no actual argument validators are given"
    argument_validators = []
    
    # positional arguments
    if VERBOSE: print('Positional:')
    for position, (name,argument) in enumerate(zip(argument_names,args)):
        arg_validator = argument_validator_from_argument(argument, name, position, verbose=VERBOSE)
        argument_validators.append(arg_validator)
        
    if VERBOSE: print('\nNamed:')
    # keyword arguments
    for name,named_argument in kwargs.items():
        if isinstance(named_argument, ArgumentValidator):
            position = named_argument.position + 1
        else:
            last_position = max(map(lambda val: val.position, argument_validators))
            position = last_position + 1

        arg_validator = argument_validator_from_argument(named_argument, name, position, verbose=VERBOSE)
        argument_validators.append(arg_validator)
    
    return SignatureValidator(argument_validators)
