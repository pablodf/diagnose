# -*- coding: latin-1 -*-

import pymysql
from pydiag import personas, opciones, pymy
from spiutils.utils import echo
import sys

if __name__ == '__main__':
    # Leer opciones de Diagnose
    host = pymy.get_host()
    if not host:
        print echo('No se encontró host de base de datos.')
        sys.exit(1)
    # Conectar con base de datos
    conn, cur = pymy.get_conn_cursor(server=host, db='personas')
    if not (conn and cur):
        print echo('No se pudo conectar a {0}.'.format(host))
        sys.exit(2)
    while 1:
        e = personas.get_id()
        if not e:
            break
        er = personas.get_record(cur, e)
        if len(er) == 0:
            print echo('No se encontraron personas con ese número de documento.')
        print
        for i, p in enumerate(er):
            print '{:2}'.format(i + 1), personas.PERSONA0.format(**p)
        print 
        while 1:
            n = raw_input(echo('Seleccione número para ver detalles: ')).strip()
            if n == '':
                break
            elif n.isdigit():
                n = int(n)
                if 0 < n <= len(er):
                    print
                    personas.show_detail(er[n - 1])
                    id = er[n - 1]['id_persona']
                    hclist = personas.get_record(cur, id, detail=1)
                    for hc in hclist:
                        personas.show_detail_more(hc)
                    print
                else:
                    print echo('Número no válido.')
            else:
                print echo('Escriba un número.')
