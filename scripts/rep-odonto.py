# -*- coding: latin-1 -*-

from sys import exit, argv
from pydiag import pymy, opciones
from spiutils.utils import echo
from collections import Counter
import os

def get_ym():
    if argv and len(argv) == 3 and argv[1].isdigit() and argv[2].isdigit() and 2010 < int(argv[1]) < 2020 and 1 <= int(argv[2]) <= 12:
        y = int(argv[1])
        m = int(argv[2])
    else:
        while True:
            r = raw_input(echo('A�o: ')).strip()
            if not r:
                exit(1)
            if r.isdigit() and 2010 < int(r) < 2020:
                y = int(r)
                break
        while True:
            r = raw_input(echo('Mes: ')).strip()
            if not r:
                exit(1)
            if r.isdigit() and 1 <= int(r) <= 12:
                m = int(r)
                break
    return dict((('y', y), ('m', m)))

sql = """SELECT c.codigo, dt_fecha, COUNT(*) AS q
FROM atencion AS a
JOIN turnos AS t ON t.idturno = a.idturno
JOIN ci10 AS c ON a.code = c.ID
WHERE t.baja = '0'
AND a.baja = 0
AND desc_red = 'odontologia'
AND YEAR(dt_fecha) = {y} AND MONTH(dt_fecha) = {m}
GROUP BY c.codigo, dt_fecha;"""

dt = get_ym()
sql = sql.format(**dt)
print 'Conectando a la base de datos...'
host = pymy.get_host()
conn, cur = pymy.get_conn_cursor(host)
print 'Consultando...'
cur.execute(sql)
print 'Recuperando datos...'
data = list(cur.fetchall())
print 'Listo.'

codigos = sorted(list(dict([(rec[u'codigo'], 1) for rec in data])))
q = dict()
for c in codigos:
    q[c] = Counter()
    for rec in data:
        if rec[u'codigo'] == c:
            q[c][rec[u'dt_fecha'].day] = rec[u'q']

op = opciones.diagnose_opciones()
html = '''<html>
<head>
<title>Resumen diario mensual odontol�gico</title>
<style type="text/css">
body {{ font-family: sans-serif; }}
thead {{ color: white; background-color: #444; }}
tbody th {{ color: white; background-color: #666; }}
th, td  {{ border: 1px dotted gray; }}
#res td {{ text-align: right; }}
</style>
</head>
<body>
<h1>Resumen diario mensual odontol�gico</h1>
<table>
<tr><td>Establecimiento</td><td>{nombre_empresa}</td><td>{clave_est}-0</td></tr>
<tr><td>Servicio</td><td>ODONTOLOGIA</td><td>500.3.5</td></tr>
'''.format(**op)

html += '''<tr><td>Fecha:</td><td>{m:02d}/{y}</td></tr>
</table>
<br/>
'''.format(**dt)

fn = os.path.join(os.environ.get('TEMP', '.'), 'odonto.html')
with open(fn, 'w') as outf:
    outf.write(html)
    outf.write('<table id="res">\n')
    outf.write('<thead><tr><th>Cod/Dia</th>')
    outf.write(''.join(['<th>{:02d}</th>'.format(d) for d in range(1, 32)]) + '</tr></thead>\n')
    outf.write('<tbody>\n')
    colors = '#ffc', '#fff'
    i = 0
    for c in codigos:
        cc = '&nbsp;' + c
        outf.write('<tr span style="background-color: {0}"><th>'.format(colors[i % 2]) + cc + '</th>') 
        for d in range(1, 32):
            outf.write('<td>' + str(q[c][d] or '&nbsp;') + '</td>')
        outf.write('</th></tr>\n')
        i += 1
    outf.write('</tbody>\n')
    outf.write('</table>')
    
os.startfile(fn)

