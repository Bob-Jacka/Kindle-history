"""
Controller, responsible for file with read books
"""
from pathlib import Path

from core.entities.Formatter import Format
from data.Constants import INPUT_SYM


class ReadFile:

    def __init__(self, filename: str | Path):
        self.readfile = open(filename)
        self.fullpath_to_readfile = self.get_fullpath_to_readfile()

    def is_need_for_new_line(self) -> bool:
        """
        Super dummy function for checking if you need new line symbol in read file.
        :return: bool value if you need for new line in read file
        """
        books_counter: int = 0
        new_line_counter: int = 0
        while True:
            line = self.readfile.readline()

            if line.endswith('\n'):
                new_line_counter += 1

            if line == '':
                break

            books_counter += 1
        if books_counter > new_line_counter:
            return True
        elif books_counter == new_line_counter:
            return False
        else:
            return False

    def check_for_duplicates(self) -> None:
        """
        Check for duplicates in read file and output useful message about
        :return: None
        """
        all_data = self.readfile.readlines()
        is_found: bool = False
        for book_name in all_data:
            count = all_data.count(book_name)
            if count >= 2:
                is_found = True
                print(f'Duplicate found with name {book_name} for {count} times')
        if not is_found:
            print('No duplicates found')

    def find_book(self) -> None:
        """
        Function for finding book in read file, by providing book name or name part.
        :return: None
        """
        while True:
            Format.prYellow('Enter book name to find:')
            book_to_find = input(INPUT_SYM)
            if book_to_find != '' and book_to_find is not None:
                for book in self.readfile:
                    if book.find(book_to_find):
                        Format.prGreen('Book found')
                        break
                    else:
                        Format.prRed('Book not found')
                        break
                break  # exit loop if book found or not

    def close_read_file(self):
        self.readfile.close()

    def add_book(self):
        """
        Add book to read book file
        :return: None
        """
        pass

    def remove_book(self):
        """
        Remove book from read book file
        :return:
        """
        pass

    def get_fullpath_to_readfile(self):
        #TODO переделать
        if self.fullpath_to_readfile is not None:
            return self.fullpath_to_readfile
        else:
            raise Exception('File with read books is not initialized')