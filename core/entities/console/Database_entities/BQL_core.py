""""
BQL (Book query language) is used in book database module.
Dummy syntax interpreter for BQ language in this file
"""

from typing import Final, Literal

from core.entities.console.Database_entities.Database import Database
from core.exceptions.DatabaseException import SyntaxInterpreterException
from data.Wrappers import (
    log,
    cancelable_operation
)

import re
from typing import Optional


class Syntax_interpreter:
    """
    Class responsible for syntax interpretation in interactive (or not) mode.
    Interpreter for BQL (book query language).
    Map contains key for fast retrieving element and tuple with two fields, where first field is syntax word
    and second field is help description for words and its usage.
            Order of execution:
        1. first you need to create database object
        2. second create tables in your database
        3. and last create records in tables
        4. And fourth, use it...
    """
    __syntax_rules: Final[dict[str, tuple[str, str]]] = {
        # main operators in database:
        'choose': tuple(
            ('choose', 'like "select" word in sql, can take parameters for selecting: all or row name')),

        'delete': tuple(('delete', 'can delete record in table or table (cancelable operation)')),

        'create': tuple(
            ('create', 'can create table | database or record object with parameters (cancelable operation)')),

        'update': tuple(('update', 'update records in table object (cancelable operation)')),

        'add': tuple(('add', 'add record to the table, require table name (cancelable operation)')),

        # embedded functions to use:
        'sync': tuple(('sync', 'synchronize records between your local pc and e-book')),

        'reg': tuple(('reg', 'word for regular expressions, take string object as a parameter and find string')),

        'count': tuple(('count', 'count books')),

        # other words:
        'help': tuple(('help', 'special operator for help users in their usage of BQL syntax')),
        'all': tuple(('all', 'special word for selecting or deleting all records in database')),
        'in': tuple(('in', 'like "from" word in sql')),
        'using': tuple(('using', 'use this word for use database as a main database')),

        # entity words:
        'Database': tuple(('database', 'word for creating database')),
        'Table': tuple(('table', 'word for table in database, contains parameters: name, order or limit')),
        'Record': tuple(('record', 'word for record in table'))
    }
    """
    Examples of BQL syntax:
    1. choose <record> in <table_name> (select statement)
        1.1 choose Record(name="1984", <optional book type>, <optional read time>) in Table(name="customers")
        1.2 CHOOSE RECORD(name="some book") in Table(name="books") (Operators can be in upper or lower case)
        
    2. delete <record> in <table_name> (delete statement)
        delete Record(name="Harry potter", <optional book type>, <optional read time>) in Table(name="customers")
        
    3. sync (synchronize data between database and e-book, require no parameters)
    
    4. create Table(name=<required parameters name>) in Database(name=<db_name>) - (creates table with given parameters)
        4.1 create Database(name=standard_db)
    
    5. add Record(name='We') in Table(name="tableName")
    
    6. update Record(name='Brave new world') in Table(name='Anti_utopias') 
        6.1 update Record(name=reg('45 ')) in Table(name=reg('Anti'))
        - you can use 'reg' word for regular expressions if you do not remember full name
        
    7. using Database(name=db_name_to_use) - use database as main database in utility, all table actions will be 
    using with tables in this database
        7.1 Delete Database(name=db_name) - delete database 
        7.2 Create Database(name=db_name) - And you can create database, other CRUD actions are not allowed
    
    Other examples: Choose all in Table(name="math", order=desk, limit=10) - descending select from all from 
    table named math and limit by 10 records"""

    def __init__(self):
        # Interpreter entities init:
        self.databases: list = list()

    @cancelable_operation
    def _create_database(self, db_name: str) -> None:
        """
        Create database
        :param db_name: database name
        :return: None
        """
        try:
            new_database = Database(db_name)
            self.databases.append(new_database)
        except Exception as e:
            print(f'An exception occurred while creating database - {e}')

    @cancelable_operation
    def synchronize(self) -> None:
        """
        Method for synchronizing e-book files and database tables
        :return: None
        """
        pass

    @log
    def get_database(self):
        if len(self.databases) != 0:
            return self.databases
        else:
            raise

    @log
    def parse_sentence(self, sentence: str) -> None:
        """
        Parse given sentence in book query language and invoke functions.
        :param sentence: string sentence in book query language.
        :return: None
        """
        lexemes = sentence.split(' ')
        operator = lexemes[0].lower()

        if len(lexemes) == 1 and operator == 'help':
            self.print_help()
        elif len(lexemes) == 1 and operator == 'sync':
            self.__parse_sync_operator()
        else:
            if operator in self.__syntax_rules.keys():
                match operator:
                    case 'choose':
                        self.__parse_select_operator(lexemes=lexemes)
                    case 'delete':
                        self.__parse_delete_operator(lexemes=lexemes)
                    case 'create':
                        self.__parse_create_operator(lexemes=lexemes)
                    case 'add':
                        self.__parse_add_operator(lexemes=lexemes)
                    case 'update':
                        self.__parse_update_operator(lexemes=lexemes)
                    case 'using':
                        self.__parse_using_operator(lexemes=lexemes)
                    case _:
                        raise SyntaxInterpreterException(f'Unknown operator: {operator}')
            else:
                raise SyntaxInterpreterException('Sentence should start with operator')

    @log
    def __parse_select_operator(self, lexemes: list[str]):
        """
        Parse select operator: choose Record(...) in Table(...)
        """
        try:
            # Find Record parameters
            record_params = self.__extract_entity_params(lexemes, 'Record')
            table_params = self.__extract_entity_params(lexemes, 'Table')

            if not table_params:
                raise SyntaxInterpreterException('Table name required for select')

            table_name = table_params.get('name')
            database = self.__get_current_database()

            if database is None:
                raise SyntaxInterpreterException('No database selected. Use "using Database(name=...)"')

            table = self.__find_table(database, table_name)
            if table is None:
                raise SyntaxInterpreterException(f'Table not found: {table_name}')

            # Filter records if parameters provided
            if record_params:
                return self.__filter_records(table, record_params)
            else:
                # choose all
                return table.get_records() if hasattr(table, 'get_records') else []

        except Exception as e:
            raise SyntaxInterpreterException(f'Select parsing error: {e}')

    @log
    def __parse_delete_operator(self, lexemes: list[str]):
        """
        Parse delete operator: delete Record(...) in Table(...)
        or: delete Table(...) in Database(...)
        """
        try:
            # Check if deleting table or record
            if 'Record(' in ' '.join(lexemes):
                record_params = self.__extract_entity_params(lexemes, 'Record')
                table_params = self.__extract_entity_params(lexemes, 'Table')

                if not table_params:
                    raise SyntaxInterpreterException('Table name required')

                database = self.__get_current_database()
                table = self.__find_table(database, table_params.get('name'))

                if record_params.get('name') == 'all':
                    table.delete_all_records()
                else:
                    table.delete_record(record_params)

            elif 'Table(' in ' '.join(lexemes):
                table_params = self.__extract_entity_params(lexemes, 'Table')
                db_params = self.__extract_entity_params(lexemes, 'Database')

                database = self.__find_database(db_params.get('name')) if db_params else self.__get_current_database()
                database._delete_table(table_params.get('name'))

        except Exception as e:
            raise SyntaxInterpreterException(f'Delete parsing error: {e}')

    @log
    def __parse_create_operator(self, lexemes: list[str]):
        """
        Parse create operator: create Table(...) in Database(...)
        or: create Database(name=...)
        """

        try:
            sentence = ' '.join(lexemes)

            if 'Database(' in sentence:
                db_params = self.__extract_entity_params(lexemes, 'Database')
                db_name = db_params.get('name')
                if not db_name:
                    raise SyntaxInterpreterException('Database name required')
                self._create_database(db_name)

            elif 'Table(' in sentence:
                table_params = self.__extract_entity_params(lexemes, 'Table')
                db_params = self.__extract_entity_params(lexemes, 'Database')

                table_name = table_params.get('name')
                if not table_name:
                    raise SyntaxInterpreterException('Table name required')

                if db_params:
                    database = self.__find_database(db_params.get('name'))
                else:
                    database = self.__get_current_database()

                if database is None:
                    raise SyntaxInterpreterException('No database selected')

                database._create_table(table_name)

            elif 'Record(' in sentence:
                record_params = self.__extract_entity_params(lexemes, 'Record')
                table_params = self.__extract_entity_params(lexemes, 'Table')

                database = self.__get_current_database()
                table = self.__find_table(database, table_params.get('name'))

                self.__create_record(table, record_params)

        except Exception as e:
            raise SyntaxInterpreterException(f'Create parsing error: {e}')

    @log
    def __parse_update_operator(self, lexemes: list[str]):
        """
        Parse update operator: update Record(...) in Table(...)
        Supports reg() for pattern matching.
        """
        try:
            record_params = self.__extract_entity_params(lexemes, 'Record')
            table_params = self.__extract_entity_params(lexemes, 'Table')

            if not table_params:
                raise SyntaxInterpreterException('Table name required')

            database = self.__get_current_database()
            table = self.__find_table(database, table_params.get('name'))

            # Check for regex in record name
            if 'reg(' in str(record_params.get('name', '')):
                pattern = self.__parse_reg_expression(record_params['name'])
                table.update_record_by_pattern(pattern, record_params)
            else:
                table.update_record(record_params)

        except Exception as e:
            raise SyntaxInterpreterException(f'Update parsing error: {e}')

    @log
    def __extract_entity_params(self, lexemes: list[str], entity_name: str) -> dict:
        """
        Extract parameters from Entity(param1=value1, param2=value2) syntax.
        :param lexemes: list of lexemes from sentence
        :param entity_name: name of entity (Record, Table, Database)
        :return: dictionary of parameters
        """
        sentence = ' '.join(lexemes)
        pattern = rf"{entity_name}\(([^)]*)\)"
        match = re.search(pattern, sentence, re.IGNORECASE)

        if not match:
            return {}

        params_str = match.group(1)
        params = {}

        # Parse key=value pairs
        for pair in params_str.split(','):
            pair = pair.strip()
            if '=' in pair:
                key, value = pair.split('=', 1)
                key = key.strip()
                value = value.strip().strip('"\'')
                params[key] = value

        return params

    @log
    def __parse_add_operator(self, lexemes: list[str]):
        """
       Parse add operator: add Record(name='...') in Table(name='...')
       """

        try:
            record_params = self.__extract_entity_params(lexemes, 'Record')
            table_params = self.__extract_entity_params(lexemes, 'Table')

            if not record_params or not table_params:
                raise SyntaxInterpreterException('Record and Table parameters required')

            table_name = table_params.get('name')
            database = self.__get_current_database()

            if database is None:
                raise SyntaxInterpreterException('No database selected')

            table = self.__find_table(database, table_name)
            if table is None:
                raise SyntaxInterpreterException(f'Table not found: {table_name}')

            from core.entities.console.Database_entities.Record import _Record

            new_record = _Record(
                identifier=self.__generate_id(table),
                book_name=record_params.get('name', ''),
                book_category=record_params.get('category', ''),
                read_date=record_params.get('read_date', ''),
                book_type=record_params.get('type', 'text')
            )
            table.add_record(new_record)

        except Exception as e:
            raise SyntaxInterpreterException(f'Add parsing error: {e}')

    @log
    def __get_current_database(self) -> Optional[Database]:
        """
        Get currently active database.
        """
        if hasattr(self, '_current_database'):
            return self._current_database
        if len(self.databases) == 1:
            return self.databases[0]
        return None

    @log
    def __find_database(self, db_name: str) -> Optional[Database]:
        """
        Find database by name.
        """
        for db in self.databases:
            if db.database_name == db_name:
                return db
        return None

    @log
    def __find_table(self, database: Database, table_name: str):
        """
        Find table in database by name.
        """
        for table in database.get_tables():
            if table.get_table_name() == table_name:
                return table
        return None

    @log
    def __generate_id(self, table) -> int:
        """
        Generate new unique ID for record.
        """
        records = table.get_records() if hasattr(table, 'get_records') else []
        if not records:
            return 1
        return max(r.id for r in records) + 1

    @log
    def __filter_records(self, table, params: dict) -> list:
        """
        Filter records by parameters.
        """
        records = table.get_records() if hasattr(table, 'get_records') else []
        result = []

        for record in records:
            match = True
            for key, value in params.items():
                if key == 'name' and record.book_name != value:
                    match = False
                elif key == 'category' and record.book_category != value:
                    match = False
                elif key == 'type' and record.type != value:
                    match = False
            if match:
                result.append(record)

        return result

    @log
    def __create_record(self, table, params: dict) -> None:
        """
        Create and add record to table.
        """
        from core.entities.console.Database_entities.Record import _Record

        record = _Record(
            identifier=self.__generate_id(table),
            book_name=params.get('name', ''),
            book_category=params.get('category', ''),
            read_date=params.get('read_date', ''),
            book_type=params.get('type', 'text')
        )
        table.add_record(record)

    @log
    def __parse_sync_operator(self):
        self.synchronize()

    @log
    def __parse_using_operator(self, lexemes: list[str]) -> None:
        """
        Parse: using Database(name=db_name)
        """
        db_params = self.__extract_entity_params(lexemes, 'Database')
        db_name = db_params.get('name')

        if not db_name:
            raise SyntaxInterpreterException('Database name required')

        database = self.__find_database(db_name)
        if database is None:
            raise SyntaxInterpreterException(f'Database not found: {db_name}')

        self._current_database = database

    @log
    def __parse_reg_expression(self, value: str):
        """
        Extract regex pattern from reg('pattern') syntax.
        :param value: string containing reg('pattern')
        :return: extracted pattern
        """

        match = re.search(r"reg\(['\"](.+?)['\"]\)", value)
        if match:
            return match.group(1)
        raise SyntaxInterpreterException(f'Invalid regex syntax: {value}')

    @log
    def test_interpreter(self):
        return "Hello from interpreter"

    @log
    def print_help(self):
        print('This module is responsible for database functionality')
        print('Here are words that used')
        for _, value in self.__syntax_rules:
            print(f'{value[0]} word contains next comment: {value[1]}')

    class Static_expressions:
        """
        Static BQL expressions to use;
        Can be used in web interface (auto mode) or console without interactive interpreter;
        """

        @log
        @staticmethod
        def update_record() -> str:
            return f''

        @log
        @staticmethod
        def add_record_exp1(rec_name: str, table_name: str) -> str:
            """
            Add record with lite parameters, only name
            :param rec_name: Record name (name of the book)
            :param table_name: Table to insert
            :return:
            """
            return f'add Record(name={rec_name} in Table(name={table_name})'

        @log
        @staticmethod
        def add_record_exp2(rec_name: str, book_author: str,
                            book_type: Literal['text', 'audio'],
                            table_name: str) -> str:
            """
            Full version of record add, with all parameters
            :param book_author: author of the book
            :param book_type: type literal, only text or audio
            :param rec_name: Record name (name of the book)
            :param table_name: Table to insert
            :return:
            """
            return f'add Record(name={rec_name} in Table(name={table_name})'

        @log
        @staticmethod
        def remove_record() -> str:
            return f''
