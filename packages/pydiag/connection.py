# -*- coding: latin-1 -*-

import pymysql

class DiagnoseConnection:
    def __init__(self, host='localhost', port=3306, user='gestion_', passwd='GESTION_77', db='diagnose'):
        for a in ('host', 'port', 'user', 'passwd', 'db'):
            setattr(self, a, eval(a))
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = pymysql.connect(host, port, user, passwd, db)
        return self.connection

    def cursor(self, type):
        if type == dict:
            args = [pymysql.cursors.DictCursor]
        else:
            args = []
        self.cursor = self.connection.cursor(*args)
        return self.cursor

    def execute(self, query):
        self.cursor.execute(query)