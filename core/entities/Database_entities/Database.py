import os
import types

from core.entities.Database_entities.Table import _Table
from core.exceptions.DatabaseException import DatabaseException
from data.Wrappers import cancelable_operation, log


class Database:
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
            new_table = _Table(table_name)
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
