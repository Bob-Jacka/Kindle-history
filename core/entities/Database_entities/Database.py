import os
from typing import (
    TypeVar,
    Generic,
    Literal
)

from core.exceptions.DatabaseException import DatabaseException
from core.modules.Book_db import cancelable_operation, log


class _Record:
    """
    Quant of book database storage table.
    Record consists of the next columns:
    id, Book name, Book category, Read date, Book type
    """

    type __Book_type = Literal['text', 'audio']

    def __init__(self, identifier: int, book_name: str, book_category: str = '',
                 read_date: str = '',
                 book_type: __Book_type = 'text'):
        """
        Wrapper class for record in database, take book data class parameters and create wrapper in db
        Create record entity with given parameters:
        :param identifier: int identifier of book, like 1, 2, 3 or ...
        :param book_name: name of the book to include
        :param book_category: category of the book, like math or programming
        :param read_date: date when book was read.
        :param book_type: type of the book, can contain one of the value - audio or text.
        """
        self.id = identifier
        self.book_name = book_name
        self.book_category = book_category
        self.read_date = read_date
        self.type = book_type

    def get_book_id(self):
        return self.id

    def get_book_name(self):
        return self.book_name

    def get_dir_name(self):
        return self.book_category

    def get_read_date(self):
        return self.read_date

    def get_book_type(self):
        return self.type

    def print_object(self):
        print(f'''
                            Book name: {self.book_name},
                            Book category: {self.book_category},
                            Book read date: {self.read_date}
                            ''')


T = TypeVar('T')  # Generic type of table


class _Table(Generic[T]):
    """
    Quant of book database storage.
    """

    def __init__(self, table_name: str):
        self.table_name = table_name
        self.__inner_table: list = list()  # inner table container for records
        # initialize table and create file
        self.__init_table()

    def get_table_name(self):
        return self.table_name

    @cancelable_operation
    def add_record(self, record):
        try:
            self.__inner_table.append(record)
        except Exception as e:
            print(f'An exception during add record to table - {e}')

    @cancelable_operation
    def update_record(self, table_name: str, identifier: str):
        pass

    @cancelable_operation
    def delete_record(self, table_name: str, identifier: str):
        pass

    @log
    def select_records(self) -> None:
        """
        Select from already read and e-book files
        :return: None
        """
        pass

    def __init_table(self):
        if not os.path.exists(self.table_name):
            with open(self.table_name, 'w+'):
                pass
        else:
            print('Table already exists')


class _Database:
    """
    Upper level entity in book_db.
    Contains tables and actions with them.
    """

    __tables: list[_Table]  # container for tables in database

    def __init__(self, database_name: str):
        self.database_name: str = database_name
        self.__tables = list()
        if not os.listdir().__contains__(database_name):
            self.__init_database()
        else:
            pass

    def __find_table(self, predicate) -> _Table:
        """
        Inner method of finding table in database.
        :param predicate: predicate function for comparison, should take _Table object and return bool value.
        :return: Table object that equals predicate.
        """
        table_to_return = None
        if isinstance(predicate, types.FunctionType):
            for table in self.__tables:
                if predicate(table):
                    table_to_return = table
                    break
            return table_to_return
        else:
            raise DatabaseException(f'Given predicate {predicate} is not a function')

    @cancelable_operation
    def _create_table(self, table_name: str) -> None:
        """
        Creates new file, called table in terms of book database.
        :return: None
        """
        try:
            new_table = self._Table(table_name)
            self.__tables.append(new_table)
        except Exception as e:
            print(f'An exception occurred during creating table - {e}')

    @cancelable_operation
    def _delete_table(self, table_name: str) -> None:
        if not len(self.__tables):
            self.__tables.remove(self.__find_table(lambda x: x.get_table_name() == table_name))
        else:
            raise DatabaseException(f'Error during deleting table with given name {table_name}')

    def get_tables(self):
        if not len(self.__tables) == 0:
            return self.__tables
        else:
            raise DatabaseException('')

    @log
    def __init_database(self):
        """
        Create database and initialize database architecture by creating folders (tables)
        :return:
        """
        pass
