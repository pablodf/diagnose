# -*- coding: latin-1 -*-

import argparse
from pydiag import pymy
from spiutils.utils import echo
import os


def parse_args():
    # listapacientes.py [-i] [-m dni|hc] [-s FUENTE] [-d DESTINO]
    p = argparse.ArgumentParser()
    p.add_argument('-i', default=True, action='store_true')
    p.add_argument('-m', choices=('dni', 'hc'), default='dni')
    p.add_argument('-s', '--src', default='listapacientes.txt')
    p.add_argument('-d', '--dst', default='listapacientes.html')
    return p.parse_args()

def connect():
    print 'Conectando a la base de datos...'
    host = pymy.get_host()
    conn, cur = pymy.get_conn_cursor(host)
    return conn, cur

def query_one(cur, crit, srch):
    sql = 'SELECT * FROM paciente WHERE {} = {};'.format(crit, srch)
    print 'Consultando:', sql
    cur.execute(sql)
    print 'Recuperando datos...'
    return list(cur.fetchall())

def query_all(f, mode, cur):
    crit = 'nro_doc' if mode == 'dni' else 'hc'
    if type(f) == file:
        r = []
        for line in f:
            srch = line.strip().split(' ', 1)
            if len(srch) >= 1:
                r.append(srch[0])
    else:
        r = f
    if len(r) == 0:
        print 'No hay nada que buscar.'
        return []
    sql = 'SELECT * FROM paciente WHERE {} IN ({});'.format(crit, ', '.join(r))
    print 'Consultando: ', sql
    cur.execute(sql)
    print 'Recuperando datos...'
    return list(cur.fetchall())

def make_html(found):
    html = '''<html>
<head>
<title>Turnos</title>
<style type="text/css">
body { font-family: sans-serif; }
thead { color: white; background-color: #444; }
tbody th { color: white; background-color: #666; }
th, td  { border: 1px dotted gray; }
#res td { text-align: right; }
</style>
</head>
<body>
<h1>Turnos</h1>
<table>
<thead>
'''
    html += ('<tr>' + ''.join(
            '<th>{}</th>'.format(colname) for colname in (
                'Apellido y nombre', 'HC', 'Tipo y nro. doc.',
                'Fecha nac.', 'Domicilio', 'Teléfono'))
            + '</tr>\n</thead>\n')

    template = '<tr>'
    for fldname in ('nombre', 'hc', 'documento', 'fecha_nac', 'domicilio', 'telefono'):
        template += '<td>{' + fldname + '}</td>'
    template += '</tr>\n'

    html += '<tbody>\n'
    for item in found:
        p = dict()
        p['nombre'] = '{ape_y_nom} {st_nombre}'.format(**item)
        p['hc'] = item['nr0_hc']
        p['documento'] = '{tipo_doc} {nro_doc}'.format(**item)
        p['domicilio'] = '{domicilio} {nro_dom}'.format(**item)
        p['fecha_nac'] = item['fecha_nac'].strftime('%d/%m/%Y')
        p['telefono'] = item['telefono']
        html += template.format(**p)

    html += '\n</tbody>\n</table>\n</body>\n</html>'
    return html

def get_input():
    res = []
    print echo('Ingrese cada número a buscar seguido de Enter. Enter solo para terminar.')
    while True:
        r = raw_input('Buscar: ').strip()
        if r == '':
            break
        if not r.isdigit():
            print echo('¡NO ES UN NÚMERO!')
            continue
        res.append(r)
    return res

def main():
    args = parse_args()
    conn, cur = connect()
    if args.i:
        res = get_input()
        found = query_all(res, args.m, cur)
    else:
        with open(args.src, 'r') as f1:
            found = query_all(f1, args.m, cur)
    with open(args.dst, 'w') as f2:
        html = make_html(found)
        f2.write(html)
    os.startfile(args.dst)

main()