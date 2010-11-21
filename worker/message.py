import re

class MessageWorker:
    _REGEX   = {
        re.compile(r'^(1Z?[0-9A-Z]{3}?[0-9A-Z]{3}?[0-9A-Z]{2}?[0-9A-Z]{4}?[0-9A-Z]{3}?[0-9A-Z]|[\dT]\d\d\d?\d\d\d\d?\d\d\d)$'): 'ups',
        re.compile(r'^(E\D{1}\d{9}\D{2}$|9\d{15,21})$'): 'usps',
        re.compile(r'^(\d{13})$'): 'isbn-13',
        re.compile(r'^(\d{12})$'): 'upc',
    }       

    def __init__(self):
        pass

    def parse_message(self):
        self.results = {}

    def get_info(self):
        return self.results
