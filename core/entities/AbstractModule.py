import abc
from abc import (
    abstractmethod
)


class Module(abc.ABC):

    @abstractmethod
    def post_init(self, app_config) -> None:
        """
        Post construct method for initializing config file in module
        :return: None
        """
        pass

    @abstractmethod
    def run_module_web(self) -> None:
        pass
