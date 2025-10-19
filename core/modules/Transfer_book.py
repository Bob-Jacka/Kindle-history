""""
Module for book transferring from your (maybe not your) pc to your (maybe not your) e-book
"""

from core.entities.AbstractModule import Module


class Transfer_book_tests:

    def test_transfer_with_tcp(self):
        pass

    def test_transfer_with_ftp(self):
        pass


class Transfer_book(Module):
    """
    Use ftp or tcp to transfer books to calibre book manager
    """

    def __init__(self):
        pass

    def transfer_with_ftp(self):
        pass

    def transfer_with_tcp(self):
        pass

    def run_module(self):
        """
        Run transfer book module.
        :return: None
        """
        while True:
            print('Enter module number to use it')
            print('1. Kindle history module - to store your read books')
            print('2. Transfer book - to transfer your books from pc to e-book')
            print('3. Exit - to exit from utility')
            transfer_action = int(input('>> '))
            match transfer_action:
                case 1:
                    pass
                case 2:
                    pass
                case 3:
                    print('Bye')
                    exit(0)
