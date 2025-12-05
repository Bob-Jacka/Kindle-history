class WebException(Exception):
    """
    Exception class for web interface
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
