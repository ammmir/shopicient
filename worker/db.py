import pymysql

class Database:
    def __init__(self):
        self.conn = pymysql.connect(unix_socket='/var/lib/mysql/mysql.sock', user='root', passwd=None, db='shopicient')

    def get_connection(self):
        return self.conn
