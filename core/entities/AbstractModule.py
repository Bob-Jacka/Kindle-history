from abc import (
    ABC,
    abstractmethod
)


class Module(ABC):

    @abstractmethod
    def run_module(self) -> None:
        """
        Entry point to module to execute.
        :return: None
        """
        pass
