# -*- coding: latin-1 -*-

import re
from sys import exit, argv
from itertools import cycle
from pydiag import pymy, opciones
from spiutils.utils import echo, get_dt
import os


# Armar la consulta SQL principal
def makesearch(dt0=None, dt1=None):
    sql = """SELECT DISTINCT p.* FROM compras.remitos r
    JOIN diagnose.paciente p
    ON r.in_Paciente = p.nr0_hc
    WHERE in_Paciente IS NOT NULL
    AND o_social IS NOT NULL
    """
    if dt0 and dt1:
        sql += "AND DATE(r.dt_fecha) BETWEEN '{}' AND '{}'\n".format(dt0, dt1)
    elif dt0:
        sql += "AND DATE(r.dt_fecha) >= '{}'\n".format(dt0)
    elif dt1:
        sql += "AND DATE(r.dt_fecha) <= '{}'\n".format(dt1)
    sql += ";"
    return sql


# Armar HTML de salida
def makehtml(op, dt0, dt1):
    html = '''<html>
    <head>
    <title>Pacientes únicos con obra social en Farmacia</title>
    <style type="text/css">
    body {{ font-family: sans-serif; }}
    table#res {{ width: 100%; }}
    thead {{ color: white; background-color: #444; }}
    tbody th {{ color: white; background-color: #666; }}
    th, td  {{ border: 1px dotted gray; vertical-align: top; }}
    td.num {{ text-align: right; }}
    .clr0 {{ background-color: #ffc; }}
    .clr1 {{ background-color: #fff; }}
    </style>
    </head>
    <body>
    <h1>Pacientes únicos con obra social en Farmacia</h1>
    <table>
    <tr><td>Establecimiento</td><td>{nombre_empresa}</td><td>{clave_est}-0</td></tr>
    '''.format(**op)
    html += '''<tr><td>Fecha desde:</td><td>{0}</td></tr>
    <tr><td>Fecha hasta:</td><td>{1}</td></tr>
    </table>
    <br/>
    '''.format(dt0 or '---', dt1 or '---')
    return html


# Enviar datos a un archivo HTML y abrirlo
def print2html(html, data):
    keys = 'ape_y_nom', 'st_nombre', 'nr0_hc', 'tipo_doc', 'nro_doc', 'fecha_nac', 'os'
    cols = 'Apellido', 'Nombre', 'HC', 'Doc. tipo', 'Doc. nro.', 'Fecha nac.', 'Obra social'
    fn = os.path.join(os.environ.get('TEMP', '.'), 'farmacia_os.html')
    with open(fn, 'w') as outf:
        outf.write(html)
        outf.write('<p>Cantidad de pacientes con obra social que retiraron medicación de Farmacia al menos una vez durante el período considerado: <strong>{:d}</strong>.</p>'.format(len(data)))
        outf.write('<table id="res">\n<thead><tr><th>#</th>')
        outf.write(''.join('<th>{}</th>'.format(c) for c in cols))
        outf.write('</thead>\n<tbody>\n')
        i = 0
        for rec in data:
            outf.write('<tr class="clr{}"><td class="num">{}</td>'.format(i % 2, i))
            outf.write(''.join('<td>{}</td>'.format(rec[k]) for k in keys))
            outf.write('</tr>\n')
            i += 1
        outf.write('</tbody>\n</table>\n</body>\n</html>\n')
        outf.write('</body>\n</html>\n')
    os.startfile(fn)


def __main__():
    op = opciones.diagnose_opciones()
    if not op:
        print echo('No se encuentran las opciones de conexión. No se puede conectar a la base de datos de Diagnose.')
        exit(1)

    print echo('Escriba las fechas en formato AAAA-MM-DD para filtrar la búsqueda.\nDeje vacía la pregunta si no desea filtrar por fecha.')
    dt0 = get_dt('Fecha desde')
    dt1 = get_dt('Fecha hasta')

    print 'Conectando a la base de datos...'
    host = pymy.get_host()
    conn, cur = pymy.get_conn_cursor(host)

    sql = makesearch(dt0, dt1)
    print 'Consultando...'
    cur.execute(sql)
    print 'Recuperando datos...'
    data = cur.fetchall()
    print 'Listo.'

    html = makehtml(op, dt0, dt0)
    print2html(html, data)


if __name__ == '__main__':
    __main__()
