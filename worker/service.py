from threading import Thread

from db import Database
from account import AccountWorker

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
        cur = self.db.cursor()
        cur.execute("SELECT email,email_password,last_id FROM User")
        for res in cur:
            print "result:", res
            email, password, id = r

            EmailWorker(email=email, password=password, last_seq_id=id).run()

    def get_accounts(self):
        pass

if __name__ == "__main__":
    w = EmailService()
    w.start()
