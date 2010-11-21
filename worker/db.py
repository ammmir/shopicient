import pymysql

class Database:
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd=None, db='mysql')

    def get_connection(self):
        return self.conn
