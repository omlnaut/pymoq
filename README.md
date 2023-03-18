pymoq
================

<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

Following the end-to-end
[tutorial](https://nbdev.fast.ai/Tutorials/tutorial.html) for nbdev.
Project homepage: [github](https://github.com/omlnaut/pymoq)

Currently facing pipeline issues:
[issue](https://github.com/fastai/nbdev/issues/1190)

## Install

``` sh
pip install pymoq
```

## How to use

Suppose we have the following setup in a python backend.

``` python
from typing import Protocol

class IWeb(Protocol):
    "Interface for accessing internet resources"
    
    def get(self, url:str, page:int, verbose:bool=False) -> str:
        "Fetches the ressource at `url` and returns it in string representation"
```

``` python
class RessourceFetcher:
    base_url: str = "https://some_base.com/"
    
    def __init__(self, web: IWeb):
        self._web = web
    
    def check_ressource(self, ressource_name: str, page:int, verbose:bool=False) -> bool:
        url = self.base_url + ressource_name
        ressource = self._web.get(url, page, verbose)
        
        return ressource is not None
```

We want to test the `fetch_ressource` method of `RessourceFetcher`. More
specifically, we want to test that if the ressource is correctly
returned from the source, this method should return `True`, otherwise
`False`.

### Setting up the mock

``` python
import pymoq.mocking.objects
```

``` python
mock = pymoq.mocking.objects.Mock(IWeb)
mock.get\
    .setup('https://some_base.com/ressource', int, False)\
    .returns(True)

fetcher = RessourceFetcher(mock)
```

If the call matches the siganture defined in the `setup` method, the
lambda in `returns` is called and its return value is returned:

``` python
assert fetcher.check_ressource('ressource', 1)
```

If any part of the signature does not match, `None` is returned:

``` python
assert not fetcher.check_ressource('other_ressource', 1) # wrong ressource name
assert not fetcher.check_ressource('ressource', "1") # wrong type of page argument
assert not fetcher.check_ressource('ressource', "1", verbose=True) # wrong value for verbose argument
```

### Verification

One might want to check how often a function mock was invoked with a
specific call signature. This can easily be done via the `.verify`
method:

``` python
from pymoq.argument_validators import AnyInt
```

``` python
mock = pymoq.mocking.objects.Mock(IWeb)
fetcher = RessourceFetcher(mock)

# setup
mock.get.setup(str, int, bool).returns(True)

# act
fetcher.check_ressource('ressource', 1)
fetcher.check_ressource('ressource', 2)
fetcher.check_ressource('ressource', 1, verbose=True)

# assert
mock.get.verify(str, int, bool).times(3)
mock.get.verify(str, int, bool).more_than(1)
mock.get.verify(str, int, bool).more_than_or_equal_to(3)
mock.get.verify(str, int, bool).less_than(4)
mock.get.verify(str, int, bool).less_than_or_equal_to(3)
mock.get.verify(str, str).never()

mock.get.verify(str, AnyInt('page', 2).less_than(2), bool).times(2)
```

### Setup sequences

``` python
mock = pymoq.mocking.objects.Mock(IWeb)
mock.get.setup('resource', int, bool).returns_sequence([1,2,3])

assert mock.get('resource', 1, True)==1
assert mock.get('resource', 2, False)==2
assert mock.get('resource', 3, True)==3

print(mock.get('ressource', 1, True))
```

    None

### Setup exceptions

``` python
class WebException(Exception):
    """Exception that describes web-access errors"""
```

``` python
mock = pymoq.mocking.objects.Mock(IWeb)
fetcher = RessourceFetcher(mock)

# setup failing web call
mock.get.setup('https://some_base.com/unavailable_ressource', int, bool).throws(WebException())

# act and assert exception
with pytest.raises(WebException):
    fetcher.check_ressource('unavailable_ressource', 1, True)
    
# does not raise exception if call signature does not match
fetcher.check_ressource('available_ressource', 1, True);
```

# Things to add

- return convenience (.returns(5))
- documentation
  - Validators (type_specifics, passing lambdas, passing constants,
    passing types)
  - setup options (returns, throws, …)
  - verify options (times, more_than, …)
