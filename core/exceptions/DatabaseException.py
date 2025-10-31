class DatabaseException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class TableExceptions(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class RecordExceptions(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class SyntaxInterpreterException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
