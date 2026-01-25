import datetime
from typing import Literal

from core.entities.console.AbstractModule import Module
from core.other.Utils import int_input_from_user
from data.Wrappers import log


class Book_analytic(Module):

    def __init__(self):
        """
        Module for analytics in book utility
        """
        self.config = None

    def post_init(self, app_config):
        self.config = app_config

    @log
    def run_module(self) -> None:
        while True:
            print('Book analytic module:')
            print('1. Get average speed of reading')
            print('2. Exit from module')
            user_choice = int_input_from_user()
            match user_choice:
                case 1:
                    self.get_average_reading_speed()
                    break
                case 2:
                    break
                case 1:
                    pass
                case _:
                    pass

    @log
    def get_average_reading_speed(self, start_date, count_method: Literal['days', 'months', 'year']):
        """
        Count average speed of reading.
        Divide read book count by days/months/years count since start date
        :return: None
        """
        if start_date is not None:
            divide_string = ""
            match count_method:
                case 'days':
                    pass
                case 'months':
                    pass
                case 'year':
                    current_date = datetime.datetime.now()
                    year = current_date.year
                    month = current_date.month
                    day = current_date.day
                    years_passed = start_date - datetime.date(year, month, day)
                    # divide_string = f'{}/{years_passed}'
                case _:
                    raise Exception('Wrong count method received ' + count_method)
            print('Average reading speed is ' + divide_string)
        else:
            raise Exception('Start date cannot be None')
