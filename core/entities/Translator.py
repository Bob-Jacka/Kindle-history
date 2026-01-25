import translators


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
        self.translate_serv = translators.server.TranslatorsServer()
        if self.translate_serv is not None:
            self.system_lang = translators.get_region_of_server(if_print_region=False)

    def translate(self, string_to_translate: str):
        if string_to_translate is not None:
            return self.translate_serv.translateMe(
                string_to_translate,
                to_language=self.system_lang
            )
        else:
            print('String to translate cannot be none')
            return None
