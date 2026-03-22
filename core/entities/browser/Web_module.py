from core.exceptions.WebException import WebException


class Web_interface:
    """
    Class responsible for web interface of the utility
    """

    def __init__(self, logger):
        self.logger = logger
        self.transfer = None
        self.stat = None
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
            Flask_interface.Dp.history_mod = self.history_book
            Flask_interface.Dp.stat_mod = self.stat
            Flask_interface.Dp.transfer_mod = self.transfer
            Flask_interface.Dp.local_logger = self.logger
            Flask_interface.run_web_app()
            self.logger.log('Server ending work')
        except Exception as e:
            raise WebException(f'Exception occurred while running web interface {e}')

    def attach_entities(self, stat_module, history_module, transfer_module):
        """
        Provide modules to web
        :param transfer_module: module for transferring books
        :param stat_module: module for statistics
        :param history_module: module for history of books
        :return: None
        """
        self.stat = stat_module
        self.history_book = history_module
        self.transfer = transfer_module
