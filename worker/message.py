import re

import email
from email.MIMEText import MIMEText


VENDOR_REGEX = {
    re.compile(r'@amazon\.com'): 'amazon',
}

ORDER_REGEX = {
    re.compile(r'([0-9]{3}-[0-9]+-[0-9]+)'): 'amazon',
}

TRACKING_REGEX   = {
    re.compile(r'(1Z?[0-9A-Z]{3}?[0-9A-Z]{3}?[0-9A-Z]{2}?[0-9A-Z]{4}?[0-9A-Z]{3}?[0-9A-Z]|[\dT]\d\d\d?\d\d\d\d?\d\d\d)'): 'ups',
    re.compile(r'(E\D{1}\d{9}\D{2}$|9\d{15,21})'): 'usps',
    re.compile(r'([0-9]{15})'): 'fedex',
}

PRICE_REGEX = re.compile(r'(\$[0-9,]+(\.[0-9]{2})?)')

class MessageProcessor:
    def __init__(self, data):
        self.data = data

    def get_order_total(self, text=None, max=0):
        # order total is usually the last mentioned price in the block of
        # text, or just the max of all prices found (convenient assumption)
        for m in re.finditer(PRICE_REGEX, text):
            text = m.group(0).replace('$', '').replace(',', '')
            price = float(text)
            if price > max:
                max = price
        return "%.02f" % float(max)

    def parse_message(self):
        self.results = {}
        self.results['orders'] = {}

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

            # go through each order in the mail
            for regex in ORDER_REGEX:
                regex_name = ORDER_REGEX[regex]

                order_chunks = []
                chunk_bodies = []

                # first save the chunks' locations
                for m in re.finditer(regex, body):
                    order_chunks.append( (m.start(), m.end(), m.group(0)) )
                    #print ">>>>>>>>>>>>>%s<<<<<<<<" % m.group(0)

                # now build the chunk regions
                last_chunk_begin = 0
                last_chunk_end = 0
                last_chunk_text = None
                last_chunk = None

                for i in range(0, len(order_chunks)):
                    start, end, text = order_chunks[i]
                    last_chunk_text = text

                    if last_chunk_begin != 0:
                        # subsequent chunk
                        last_chunk = body[last_chunk_begin : start - 1]
                        chunk_bodies.append( (last_chunk, last_chunk_text) )

                        # now set our begin marker
                        last_chunk_begin = start
                    else:
                        # first chunk. ends with the next's beginning
                        last_chunk_begin = start

                # handle last chunk
                chunk_bodies.append( (body[last_chunk_begin : ], last_chunk_text) )

                for chunk, order_id in chunk_bodies:
                    print "chunk >>>>>>>>>>%s<<<<<<<<" % chunk
                    print "  order id:", order_id
                    # perform order-specific extraction
                    self.extract_order_info(data=chunk, order_id=order_id)

    def extract_order_info(self, data=None, order_id=None):
        if not order_id in self.results['orders']:
            self.results['orders'][order_id] = {}

        order = self.results['orders'][order_id]

        if 'price' in order:
            max = order['price']
        else:
            max = 0

        order['price'] = self.get_order_total(text=data, max=max)

        for regex in TRACKING_REGEX:
            regex_name = TRACKING_REGEX[regex]

            for m in re.finditer(regex, data):
                text = m.group(0)
                if 'ups' == regex_name and '1Z' != text[0:2]: # HACK KLUDGE
                    continue

                if not 'tracking' in order:
                    order['tracking'] = dict(type=regex_name, tracking=text)

                #print '  %s: %02d-%02d: %s' % (regex_name, m.start(), m.end(), m.group(0))

    def get_info(self):
        return self.results
