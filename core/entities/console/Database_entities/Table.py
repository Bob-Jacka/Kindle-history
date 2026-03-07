import os
import re
from typing import (
    Generic,
    TypeVar,
    Optional,
    Any
)

from core.entities.console.Database_entities.Record import _Record
from core.exceptions.DatabaseException import DatabaseException
from data.Wrappers import (
    cancelable_operation,
    log
)

T = TypeVar('T')


class _Table(Generic[T]):
    """
    Quant of book database storage.
    """

    def __init__(self, table_name: str):
        self.table_name = table_name
        self.__inner_table: list[_Record] = list()
        self.__init_table()

    def get_table_name(self) -> str:
        return self.table_name

    def get_records(self) -> list[_Record]:
        """
        Get all records from table.
        :return: List of records
        """
        return self.__inner_table

    @cancelable_operation
    def add_record(self, record: _Record) -> None:
        """
        Add record to table.
        :param record: Record object to add
        """
        try:
            self.__inner_table.append(record)
            self.__save_table()
        except Exception as e:
            raise DatabaseException(f'Error adding record: {e}')

    @cancelable_operation
    def update_record(self, params: dict) -> None:
        """
        Update record by name.
        :param params: Dictionary with name and fields to update
        """
        record_name = params.get('name')
        if not record_name:
            raise DatabaseException('Record name required for update')

        for record in self.__inner_table:
            if record.book_name == record_name:
                if 'category' in params:
                    record.book_category = params['category']
                if 'read_date' in params:
                    record.read_date = params['read_date']
                if 'type' in params:
                    record.type = params['type']
                self.__save_table()
                return

        raise DatabaseException(f'Record not found: {record_name}')

    @cancelable_operation
    def update_record_by_pattern(self, pattern: str, params: dict) -> None:
        """
        Update records matching regex pattern.
        :param pattern: Regex pattern to match record names
        :param params: Fields to update
        """
        try:
            regex = re.compile(pattern)
            updated = 0

            for record in self.__inner_table:
                if regex.search(record.book_name):
                    if 'category' in params:
                        record.book_category = params['category']
                    if 'read_date' in params:
                        record.read_date = params['read_date']
                    if 'type' in params:
                        record.type = params['type']
                    updated += 1

            if updated > 0:
                self.__save_table()
            else:
                raise DatabaseException(f'No records matching pattern: {pattern}')

        except re.error as e:
            raise DatabaseException(f'Invalid regex pattern: {e}')

    @cancelable_operation
    def delete_record(self, params: dict) -> None:
        """
        Delete record by parameters.
        :param params: Dictionary with record identification
        """
        record_name = params.get('name')

        if record_name == 'all':
            self.delete_all_records()
            return

        if not record_name:
            raise DatabaseException('Record name required for deletion')

        for i, record in enumerate(self.__inner_table):
            if record.book_name == record_name:
                self.__inner_table.pop(i)
                self.__save_table()
                return

        raise DatabaseException(f'Record not found: {record_name}')

    @cancelable_operation
    def delete_record_by_id(self, record_id: int) -> None:
        """
        Delete record by ID.
        :param record_id: Record identifier
        """
        for i, record in enumerate(self.__inner_table):
            if record.id == record_id:
                self.__inner_table.pop(i)
                self.__save_table()
                return

        raise DatabaseException(f'Record with ID {record_id} not found')

    @cancelable_operation
    def delete_all_records(self) -> None:
        """
        Delete all records from table.
        """
        self.__inner_table.clear()
        self.__save_table()

    @log
    def select_records(self, params: Optional[dict] = None) -> list[_Record]:
        """
        Select records from table.
        :param params: Optional filter parameters
        :return: List of matching records
        """
        if params is None:
            return self.__inner_table

        result = []
        for record in self.__inner_table:
            match = True

            if 'name' in params:
                if params['name'] != record.book_name:
                    match = False
            if 'category' in params and match:
                if params['category'] != record.book_category:
                    match = False
            if 'type' in params and match:
                if params['type'] != record.type:
                    match = False
            if 'read_date' in params and match:
                if params['read_date'] != record.read_date:
                    match = False

            if match:
                result.append(record)

        return result

    @log
    def select_by_pattern(self, pattern: str) -> list[_Record]:
        """
        Select records matching regex pattern.
        :param pattern: Regex pattern for book name
        :return: List of matching records
        """
        try:
            regex = re.compile(pattern)
            return [r for r in self.__inner_table if regex.search(r.book_name)]
        except re.error as e:
            raise DatabaseException(f'Invalid regex pattern: {e}')

    @log
    def count_records(self) -> int:
        """
        Count records in table.
        :return: Number of records
        """
        return len(self.__inner_table)

    @log
    def find_record_by_name(self, name: str) -> Optional[_Record]:
        """
        Find record by book name.
        :param name: Book name to search
        :return: Record or None
        """
        for record in self.__inner_table:
            if record.book_name == name:
                return record
        return None

    @log
    def find_record_by_id(self, record_id: int) -> Optional[_Record]:
        """
        Find record by ID.
        :param record_id: Record identifier
        :return: Record or None
        """
        for record in self.__inner_table:
            if record.id == record_id:
                return record
        return None

    def __init_table(self) -> None:
        """
        Initialize table file.
        """
        if not os.path.exists(self.table_name):
            with open(self.table_name, 'w+', encoding='utf-8'):
                pass
        else:
            print('Table already exists')

    def __save_table(self) -> None:
        """
        Save table to file.
        """
        try:
            with open(self.table_name, 'w', encoding='utf-8') as f:
                for record in self.__inner_table:
                    line = f'{record.id}|{record.book_name}|{record.book_category}|{record.read_date}|{record.type}\n'
                    f.write(line)
        except Exception as e:
            raise DatabaseException(f'Error saving table: {e}')

    def __load_table(self) -> None:
        """
        Load table from file.
        """
        if not os.path.exists(self.table_name):
            return

        try:
            with open(self.table_name, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) >= 5:
                        record = _Record(
                            identifier=int(parts[0]),
                            book_name=parts[1],
                            book_category=parts[2],
                            read_date=parts[3],
                            book_type=parts[4]
                        )
                        self.__inner_table.append(record)
        except Exception as e:
            raise DatabaseException(f'Error loading table: {e}')

    def __str__(self) -> str:
        return f'Table(name={self.table_name}, records={len(self.__inner_table)})'

    def __repr__(self) -> str:
        return self.__str__()
