class KindleHistoryException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class MemorizeException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
