"""
Entity for text formating and color console output
"""

from typing import Final


class Format:
    """
    Utility class for text formater
    Includes print functions in different colors and underline technology.
    """
    underline_end: Final[str] = '\033[0m'
    underline_start: Final[str] = '\033[4m'

    @staticmethod
    def prRed(string: str):
        print("\033[91m {}\033[00m".format(string))

    @staticmethod
    def prGreen(string: str):
        print("\033[92m {}\033[00m".format(string))

    @staticmethod
    def prYellow(string: str):
        print("\033[93m {}\033[00m".format(string))

    @staticmethod
    def prCyan(string: str):
        print("\033[96m {}\033[00m".format(string))

    @staticmethod
    def prLightGray(string: str):
        print("\033[97m {}\033[00m".format(string))
