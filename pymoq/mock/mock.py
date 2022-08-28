from typing import Generic, TypeVar

T = TypeVar("T")


class Mock(Generic[T]):
    def __init__(self, base: T):
        self._base = base
