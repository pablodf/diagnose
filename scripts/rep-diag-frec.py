# -*- coding: latin-1 -*-

import re
import os
from sys import exit, argv
from itertools import cycle
from pydiag import pymy, opciones
from spiutils.utils import echo, get_dt


# Obtener un código de servicio
def get_serv(data):
    while True:
        r = raw_input(echo('Ingrese código del servicio: ')).strip()
        if not r:
            break
        elif r.isdigit() and int(r) in [i['id'] for i in data]:
            return int(r)


# Encontrar los servicios que poseen atenciones con diagnóstico
def find_servs(cur):
    cur.execute("SELECT DISTINCT c.id, c.detalle FROM atencion a JOIN turnos t ON a.idturno = t.idturno JOIN common c ON c.id = t.tipo_estudio;")
    data = cur.fetchall()
    for i in data:
        print echo('{id:7d}\t{detalle}'.format(**i))
    return data


# Armar la consulta SQL principal
def makesearch(dt0=None, dt1=None, serv=None):
    sql = """SELECT
    ci10.codigo AS cie10,
    ci10.descripcion,
    common.detalle AS prestacion,
    COUNT(*) AS q
    FROM turnos t
    JOIN atencion a ON t.idturno = a.idturno
    JOIN ci10 ON a.code = ci10.id    
    JOIN common ON t.tipo_estudio = common.id
    JOIN paciente ON t.paciente = paciente.nr0_hc
    WHERE ci10.tipo_codificacion = 295
    """
    if serv:
        sql += "AND common.id = {:d}\n".format(serv)
    if dt0 and dt1:
        sql += "AND DATE(t.dt_fecha) BETWEEN '{}' AND '{}'\n".format(dt0, dt1)
    elif dt0:
        sql += "AND DATE(t.dt_fecha) >= '{}'\n".format(dt0)
    elif dt1:
        sql += "AND DATE(t.dt_fecha) <= '{}'\n".format(dt1)
    sql += 'GROUP BY cie10 ORDER BY q DESC;'
    return sql


# Imprimir los datos a la salida estándar
def print2screen(data):
    print
    print echo('Frecuencia de diagnósticos en consultas')
    print '-----\t------\t---------'
    print 'Cant.\tCIE-10\tDesc.'
    print '-----\t------\t---------'
    for rec in data:
        print echo('{q:5d}\t{cie10:5s}\t{descripcion}'.format(**rec))
    print


# Armar HTML de salida
def makehtml(op, dt0, dt1, servname):
    html = '''<html>
    <head>
    <title>Diagnósticos en consultas</title>
    <style type="text/css">
    body {{ font-family: sans-serif; }}
    table#res {{ width: 100%; }}
    thead {{ color: white; background-color: #444; }}
    tbody th {{ color: white; background-color: #666; }}
    th, td  {{ border: 1px dotted gray; }}
    td.num {{ text-align: right; }}
    td.cie10 {{ text-align: center; }}
    .clr0 {{ background-color: #ffc; }}
    .clr1 {{ background-color: #fff; }}
    </style>
    </head>
    <body>
    <h1>Frecuencia de diagnósticos en consultas</h1>
    <table>
    <tr><td>Establecimiento</td><td>{nombre_empresa}</td><td>{clave_est}-0</td></tr>
    '''.format(**op)
    html += '''<tr><td>Fecha desde:</td><td>{0}</td></tr>
    <tr><td>Fecha hasta:</td><td>{1}</td></tr>
    <tr><td>Servicio:</td><td>{2}</td></tr>
    </table>
    <br/>
    '''.format(dt0 or '---', dt1 or '---', servname or '(Todos)')
    return html


# import tempfile

# Enviar datos a un archivo HTML y abrirlo
def print2html(html, data):
    fn = os.path.join(os.environ.get('TEMP', '.'), 'diagnosticos.html')
    # fd, fn = tempfile.mkstemp('diagnosticos', '.html', text=True)
    with file(fn, 'w') as outf:
        outf.write(html)
        outf.write('<table id="res">\n'
                   '<thead><tr><th>Frecuencia</th><th>Código CIE-10</th><th>Descripción</th></thead>\n'
                   '<tbody>\n')
        i = cycle((0, 1))
        for rec in data:
            outf.write('<tr class="clr{}">'.format(i.next()) + \
                       '<td class="num">{q:d}</td><td class="cie10">{cie10:5s}</td><td>{descripcion}</td></tr>\n'.format(**rec))
        outf.write('</tbody>\n</table>\n</body>\n</html>\n')
    os.startfile(fn)


def __main__():
    op = opciones.diagnose_opciones()
    if not op:
        print echo('No se encuentran las opciones de conexión. No se puede conectar a la base de datos de Diagnose.')
        exit(1)

    print echo('Escriba las fechas en formato AAAA/MM/DD para filtrar la búsqueda.\nDeje vacía la pregunta si no desea filtrar por fecha.')
    dt0 = get_dt('Fecha desde')
    dt1 = get_dt('Fecha hasta')

    print 'Conectando a la base de datos...'
    host = pymy.get_host()
    conn, cur = pymy.get_conn_cursor(host)

    print 'Servicios disponibles:'
    data = find_servs(cur)
    serv = get_serv(data)
    servname = serv and [i['detalle'] for i in data if i['id'] == serv][0] or None

    sql = makesearch(dt0, dt1, serv)
    print 'Consultando...'
    cur.execute(sql)
    print 'Recuperando datos...'
    data = cur.fetchall()
    print 'Listo.'

    print2screen(data)
    html = makehtml(op, dt0, dt1, servname)
    print2html(html, data)


if __name__ == '__main__':
    __main__()
