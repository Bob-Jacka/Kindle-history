import abc
from abc import (
    abstractmethod
)


class Module(abc.ABC):

    @abstractmethod
    def run_module(self) -> None:
        """
        Entry point to module to execute.
        :return: None
        """
        pass
