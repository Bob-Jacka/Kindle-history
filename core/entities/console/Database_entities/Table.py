import os
from typing import (
    Generic,
    TypeVar
)

from data.Wrappers import (
    cancelable_operation,
    log
)

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
