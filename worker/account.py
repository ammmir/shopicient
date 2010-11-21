import imaplib

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
        try:
            server = get_mail_server(self.email)
        except UnknownEmailProvider:
            print "unknown email provider:", self.email
            return

        self.conn = imaplib.IMAP4_SSL(server)
        imaplib.IMAP4.debug = 3
        self.conn.login(self.email, self.password)

        self.conn.select()

        typ, data = self.conn.search(None, 'ALL')

        if typ != 'OK':
            return

        for num in data[0].split():
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

if __name__ == "__main__":
    print "testing invalid email"
    a = AccountWorker(email='user@domain.ext', password='1234')
    a.update_messages()

    print "testing real email"
    a = AccountWorker(email='w2mv@unoc.net', password='shopofmind', last_seq_id=0)
    a.update_messages()
