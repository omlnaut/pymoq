from typing import Any, Callable, Generic, Protocol, Type, TypeVar, Union, cast


class IWeb(Protocol):
    def get(self, url: str) -> str:
        ...


class Wrapper:
    def __init__(self, func: Callable[[Any], Any]) -> None:
        self.func = func

    def setup(self, value: Any):
        pass

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        print("Inside Mock")
        print("Checking signature")
        print("Logging Call")


def test_function(web: IWeb):
    print(web.get("testi_url"))


T = TypeVar("T")


class _Mock(Generic[T]):
    _base_type: Type[T]

    def __init__(self, base: Type[T]):
        self._base_type = base

    def __getattr__(self, __name: str) -> Wrapper:
        return Wrapper(getattr(self._base_type, __name))

    def __dir__(self):
        return dir(self.T)


def Mock(obj: Type[T]) -> Union[_Mock[T], T]:  # pylint: disable=invalid-name
    return _Mock[T](obj)


def Object(mock: Union[_Mock[T], T]) -> T:  # pylint: disable=invalid-name
    # pylint: disable=protected-access
    return cast(type(mock._base_type), mock)  # type: ignore


if __name__ == "__main__":
    m = Mock(IWeb)

    """
    m. autocompletes "get"
    m.get. autocompletes "setup"
    """
    m.get.setup(1)

    test_function(Object(m))
