from typing import Protocol


class IWeb(Protocol):
    def get(self, url: str) -> str:
        ...
