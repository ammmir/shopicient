import email
from email.MIMEText import MIMEText
import poplib


def get_mail_server(email):
    servers = {
        'unoc.net': 'pop.gmail.com',
        'gmail.com': 'pop.gmail.com',
        'yahoo.com': 'pop.mail.yahoo.com',
    }

    domain = email[email.index("@")+1:]

    if domain in servers:
        return servers[domain]
    else:
        raise UnknownEmailProvider()

class UnknownEmailProvider(Exception):
    pass

class AccountWorker:
    def __init__(self, email=None, password=None):
        self.email = email
        self.password = password

    def update_messages(self):
        try:
            server = get_mail_server(self.email)
        except UnknownEmailProvider:
            print "unknown email provider:", self.email
            return

        self.conn = poplib.POP3_SSL(server)
        self.conn.set_debuglevel(1)
        self.conn.user(self.email)
        self.conn.pass_(self.password)

        status = self.conn.stat()

        if status[0]:
            for item in self.conn.list()[1]:
                number, bytes = item.split(' ')
                print "going to download message %s (%s bytes)" % (number, bytes)

                #lines = self.conn.retr(number)[1]
                #self.process_email("\n".join(lines))

            self.conn.quit()
        else:
            print "no messages on server"
            return

    def process_email(self, data):
        msg = email.message_from_string(data)
        print "got msg:", msg


if __name__ == "__main__":
    print "testing invalid email"
    a = AccountWorker(email='user@domain.ext', password='1234')
    a.update_messages()

    print "testing real email"
    a = AccountWorker(email='w2mv@unoc.net', password='shopofmind')
    a.update_messages()
