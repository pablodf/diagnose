import os, datetime
import pymysql

def get_by_date(tbl, attr, dt_from=None, dt_until=None, selected='*'):
    base = "SELECT {selected} FROM {tbl} WHERE {attr} ".format(**{'tbl': tbl, 'attr': attr, 'selected': selected})
    if dt_from and dt_until:
        thecmp = "BETWEEN '{0}' AND '{1}'".format(dt_from.isoformat(), dt_until.isoformat())
    elif dt_from:
        thecmp = ">= '{0}'".format(dt_from.isoformat())
    elif dt_until:
        thecmp = "<= '{0}'".format(dt_until.isoformat())
    return base + thecmp

conn = pymysql.connect(host='localhost', port=3306, user='gestion_', passwd='GESTION_77', db='diagnose')
cur = conn.cursor()

thePast = datetime.date.today() - datetime.timedelta(100)
sql = get_by_date('paciente', 'dt_created',
                  thePast,
                  datetime.date.today())
print sql
cur.execute(sql)
for rec in cur.fetchall():
    print rec
