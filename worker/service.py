import time
from threading import Thread

from db import Database
from account import AccountWorker

CHECK_INTERVAL = 60

class EmailWorker(Thread):
    def __init__(self, email=None, password=None, last_seq_id=None):
        Thread.__init__(self)
        self.worker = AccountWorker(email=email, password=password, last_seq_id=last_seq_id)

    def run(self):
        self.worker.update_messages()

class EmailService:
    def __init__(self):
        self.db = Database().get_connection()

    def start(self):
        while True:
            print ">>> checking for new emails...."
            self.iter()
            print "<<< sleeping for %d seconds..." % CHECK_INTERVAL
            time.sleep(CHECK_INTERVAL)

    def iter(self):
        cur = self.db.cursor()
        cur.execute("SELECT email,email_password,last_email_id FROM users")
        for res in cur:
            email, password, id = res

            EmailWorker(email=email, password=password, last_seq_id=id).run()
        cur.close()

if __name__ == "__main__":
    w = EmailService()
    w.start()
