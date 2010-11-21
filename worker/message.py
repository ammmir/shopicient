import re

import email
from email.MIMEText import MIMEText


_REGEX   = {
    re.compile(r'(1Z?[0-9A-Z]{3}?[0-9A-Z]{3}?[0-9A-Z]{2}?[0-9A-Z]{4}?[0-9A-Z]{3}?[0-9A-Z]|[\dT]\d\d\d?\d\d\d\d?\d\d\d)'): 'ups',
    re.compile(r'(E\D{1}\d{9}\D{2}$|9\d{15,21})'): 'usps',
    re.compile(r'([0-9]{15})'): 'fedex',
    re.compile(r'([0-9]{3}-[0-9]+-[0-9]+)'): 'amazon_order',
}       

class MessageProcessor:

    def __init__(self, data):
        self.data = data

    def parse_message(self):
        self.results = {}
        self.results['orders'] = {}
        self.results['tracking'] = {}

        msg = email.message_from_string(self.data)

        for part in msg.walk():
            if part.get_content_maintype() == "multipart":
                continue

            if part.get_content_type() != "text/plain":
                #print "ignoring non-text MIME part"
                continue

            body = part.get_payload(decode=True)
            print "body size:", len(body)
            #print "plain body:", body

            for regex in _REGEX:
                regex_name = _REGEX[regex]

                for m in re.finditer(regex, body):
                    text = m.group(0)
                    if 'ups' == regex_name and '1Z' != text[0:2]:
                        continue

                    if not text in self.results['tracking']:
                        self.results['tracking'][text] = {
                            'type': regex_name,
                        }


                    print '  %s: %02d-%02d: %s' % (regex_name, m.start(), m.end(), m.group(0))

    def get_info(self):
        return self.results
