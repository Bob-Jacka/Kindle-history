from core.exceptions.WebException import WebException


class Web_interface:
    """
    Class responsible for web interface of the utility
    """

    def __init__(self, logger):
        self.logger = logger
        self.bql = None
        self.history_book = None

    def run_interface(self):
        """
        Entry point
        Open browser and create all components in it
        :return: None
        """
        from core.entities.browser.WebInterface import Flask_interface
        try:
            self.logger.log('Server starting work')
            if self.bql is None:
                raise RuntimeError('Book db module cannot be None')
            Flask_interface.Dp.bql_interpreter = self.bql
            Flask_interface.Dp.history_mod = self.history_book
            Flask_interface.run_web_app()
            self.logger.log('Server ending work')
        except Exception as e:
            raise WebException(f'Exception occurred while running web interface {e}')

    def attach_entities(self, bql_interpreter, history_module):
        """
        Provide modules to web
        :param bql_interpreter: local db language
        :param history_module:
        :return: None
        """
        self.bql = bql_interpreter
        self.history_book = history_module
