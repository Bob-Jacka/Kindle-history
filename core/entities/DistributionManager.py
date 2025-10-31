""""
Entry point to utility and modules, contains global data from modules
"""

from typing import Final

from core.modules.Book_db import Book_db
from core.modules.Kindle_history import Kindle_history
from core.modules.Transfer_book import Transfer_book

APP_VERSION: Final[str] = '3.0.0'


def help_distribution_manager():
    pass


if __name__ == '__main__':
    while True:
        print('Enter module number to use it')
        print('1. Kindle history module - to store your read books')
        print('2. Transfer book - to transfer your books from pc to e-book')
        print('3. Book database module - to access database functionality inside utility')
        print('4. Exit - to exit from utility')
        module_to_use = int(input('>> '))
        match module_to_use:
            case 1:
                history_module = Kindle_history()
                history_module.run_module()
            case 2:
                transfer_module = Transfer_book()
                transfer_module.run_module()
            case 3:
                book_db = Book_db()
                book_db.run_module()
            case 4:
                print('Bye')
                exit(0)
            case _:
                print('Wrong module number, try again')
                continue
