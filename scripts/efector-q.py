# -*- coding: latin-1 -*-
from pydiag import pymy
from spiutils.utils import echo

conn, cur = pymy.get_conn_cursor(server=pymy.get_host(), db='hmi2')

while 1:
    s = raw_input('Buscar por nombre (N) o localidad (L)? ').strip().upper()
    if s == 'N':
        question = 'Nombre del efector'
        search = "SELECT * FROM hmi2.efectores WHERE nom_efector LIKE '%{0}%' OR nom_red_efector LIKE '%{0}%'"
    elif s == 'L':
        question = 'Localidad'
        search = "SELECT hmi2.efectores.* FROM hmi2.efectores " \
                 "JOIN hmi2.localidades ON hmi2.efectores.id_localidad = hmi2.localidades.id_localidad " \
                 "WHERE hmi2.localidades.nom_loc LIKE '%{0}%'"
    else:
        break
    while 1:
        r = raw_input(question + ': ').strip().upper()
        if r:
            cur.execute(search.format(r))
            i = 0
            for find in cur.fetchall():
                print '{id_efector:3} {nom_efector} ({nom_red_efector})'.format(**find).decode('latin-1')
                i += 1
            print '-'*16
            print i, 'efector(es)'
            print '-'*16
        else:
            break