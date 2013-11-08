# -*- coding: latin-1 -*-
from pydiag import pymy
from spiutils.utils import echo

host = pymy.get_host()
conn, cur = pymy.get_conn_cursor(host, 'diagnose')
cur.execute('SELECT COUNT(*) AS q FROM paciente WHERE dt_created BETWEEN (NOW() - INTERVAL 1 WEEK) AND NOW();')
r = cur.fetchone()
print echo('{0} pacientes creados en la última semana.'.format(r['q']))
cur.execute('SELECT COUNT(*) AS q FROM paciente WHERE dt_created BETWEEN (NOW() - INTERVAL 1 MONTH) AND NOW();')
r = cur.fetchone()
print echo('{0} pacientes creados en el último mes.'.format(r['q']))