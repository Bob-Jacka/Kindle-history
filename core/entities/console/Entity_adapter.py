class Entity_adapter:
    """
    Adapter class for converting from kindle history entity to database or vice versa.
    """

    def __init__(self, source_entity, **adapted_methods):
        self.source = source_entity
        self.__dict__.update(adapted_methods)

    def __getattr__(self, attr):
        """All non-adapted calls are passed to the object"""
        return getattr(self.obj, attr)

    def original_dict(self):
        """Print original object dict"""
        return self.obj.__dict__

    def __check_for_type(self):
        """
        Private function for checking type of source object.
        Return true if kindle history entity or false otherwise
        :return: boolean
        """
        from core.entities.console.Kindle_history_entities.Book_data import Book_data
        if isinstance(self.source, Book_data):
            return True
        return False

    def convert_to_history_entity(self):
        from core.entities.console.Kindle_history_entities.Book_data import Book_data
        if self.__check_for_type():
            return self.source
        else:
            Book_data()

    def convert_to_database_entity(self):
        from core.entities.console.Database_entities.Record import _Record
        if not self.__check_for_type():
            return self.source
        else:
            _Record()
