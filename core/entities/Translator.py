class SingletonTranslator(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Translator:
    def __init__(self):
        """
        Class for translations in utility
        """
        pass
