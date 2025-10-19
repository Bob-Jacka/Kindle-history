from abc import (
    ABC,
    abstractmethod
)
from typing import Final

CLOSE_MENU_CODE: Final[str] = '666'
"""
Code for close menu functionality
"""

INPUT_SYM: Final[str] = '>> '
"""
Symbol that applies in input fields
"""

class Module(ABC):

    @abstractmethod
    def run_module(self) -> None:
        """
        Entry point to module to execute.
        :return: None
        """
        pass
