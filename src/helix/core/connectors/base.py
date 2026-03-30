from abc import ABC, abstractmethod
from typing import Any


class Connector(ABC):
    @abstractmethod
    def get(self, query: Any, **kwargs) -> Any: ...

    def close(self):
        pass
