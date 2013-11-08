# -*- coding: latin-1 -*-

from find_mysql import *
from subprocess import call
from os.path import join, isfile, dirname
import tempfile


class DumpError(Exception):
    pass


class SQLDump:
    def __init__(self, host='localhost', port='3306', user='root', password=''):
        exe = find_mysqldump()
        if not exe:
            raise DumpError, 'mysqldump.exe not found.'
        self.exe = exe
        ret = self.test()
        if ret != 0:
            raise DumpError, 'Something is wrong with mysqldump ({}).'.format(exe)
        print self.versioninfo
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def dump(self, db, tables=None, opts=None):
        # Simplest syntax: dump one database, all or some tables
        if tables is None:
            tables = []
        if opts is None:
            opts = []
        opts += ['-h' + self.host, '-P' + self.port, '-u' + self.user, '-p' + self.password]
        with tempfile.NamedTemporaryFile(delete=False) as tempf:
            ret = call([self.exe] + opts + [db] + tables, stdout=tempf)
            if ret == 0:
                return tempf.name

    def test(self):
        with tempfile.SpooledTemporaryFile() as tempf:
            ret = call([self.exe, '-V'], stdout=tempf)
            tempf.seek(0)
            self.versioninfo = tempf.read()
        return ret
        