""""
Module for book transferring from your (maybe not your) pc to your (maybe not your) e-book

*Module only responsible for transfer books from pc to ebook
"""

from core.entities.AbstractModule import Module
from data.Wrappers import log


class Transfer_book_tests:

    def test_transfer_with_tcp(self):
        pass

    def test_transfer_with_ftp(self):
        pass


class Transfer_book(Module):
    """
    Use ftp or tcp to transfer books to calibre book manager
    """

    def __init__(self, app_config):
        self.config = app_config
        self.local_logger = app_config.get_logger()

    @log
    def transfer_with_ftp(self):
        pass

    @log
    def transfer_with_tcp(self):
        pass

    @log
    def run_module(self):
        """
        Run transfer book module.
        :return: None
        """
        while True:
            print('Enter module number to use it')
            print('1. Transfer book')
            print('2. Exit - to exit from utility')
            transfer_action = int(input('>> '))
            match transfer_action:
                case 1:
                    pass
                case 2:
                    print('Bye')
                    exit(0)
