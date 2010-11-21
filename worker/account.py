# WARNING: Insecure handling of user credentials herein. Caveat emptor.

import imaplib

from db import Database
from message import MessageProcessor

def get_mail_server(email):
    servers = {
        'unoc.net': 'imap.gmail.com',
        'gmail.com': 'imap.gmail.com',
        'yahoo.com': 'imap.mail.yahoo.com',
    }

    domain = email[email.index("@")+1:]

    if domain in servers:
        return servers[domain]
    else:
        raise UnknownEmailProvider()

class UnknownEmailProvider(Exception):
    pass

class AccountWorker:
    def __init__(self, email=None, password=None, last_seq_id=0):
        self.email = email
        self.password = password
        self.last_seq_id = last_seq_id

    def update_messages(self):
        """ This method runs in its own thread."""

        try:
            server = get_mail_server(self.email)
        except UnknownEmailProvider:
            print "unknown email provider:", self.email
            return

        self.db = Database().get_connection()
        self.load_user_id()

        self.conn = imaplib.IMAP4_SSL(server)
        self.conn.login(self.email, self.password)

        self.conn.select()

        # TODO: more efficient fetching of messages
        #criteria = "ALL AND SMALLER 32768"
        criteria = "ALL"

        typ, data = self.conn.search(None, criteria)

        if typ != 'OK':
            return

        for num in data[0].split():
            print "  fetching:", num
            typ, data = self.conn.fetch(num, '(RFC822)')
            #print 'Message %s\n%s\n' % (num, data[0][1])

            if typ != 'OK':
                continue

            try:
                msg = data[0][1]
            except IndexError:
                continue

            self.process_email(msg)

    def process_email(self, data):
        mp = MessageProcessor(data=data)
        mp.parse_message()
        info = mp.get_info()
        print "  info:", info

        orders = info['orders']
        for order_id in orders:
            o = self.find_order(order_id)
            if o:
                self.update_order(order_id, orders[order_id])
            else:
                self.insert_order(order_id, orders[order_id])

    def find_order(self, order_id):
        # FIXME: currently using email_info field for order_id
        cur = self.db.cursor()
        cur.execute("SELECT info, vendor, price FROM orders WHERE email_info='%s'" % order_id)
        for res in cur:
            return dict(info=res[0], vendor=res[1], price=res[2])

    def insert_order(self, order_id, order):
        # FIXME: currently using email_info field for order_id
        #self.db.execute("INSERT INTO orders (user_id, email_info, vendor, price) VALUES (%d, %s, %s, %f)", order['
        pass

    def update_order(self, order_id, order):
        pass

    def load_user_id(self):
        cur = self.db.cursor()
        cur.execute("SELECT id FROM users WHERE email=%s", self.email)
        for id in cur:
            self.user_id = id
            cur.close()
            break
