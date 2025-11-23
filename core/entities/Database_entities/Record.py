from typing import Literal


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
        if self.id != '':
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
