#!/usr/bin/env python

from pydiag import pymy

host = pymy.get_host()
if host:
    conn, cur = pymy.get_conn_cursor(host)
    cur.execute("SELECT Codigo, Detalle, Sector FROM common "
                "WHERE Tipo IN ('servicios_p', 'servicios_n') "
                "AND Subsector = '5'")
    servs = dict()
    for rec in cur.fetchall():
        servs[rec['Codigo']] = rec['Sector']

    sql = "UPDATE servicios SET codigo = CONCAT(codigo, '.{}.5')) WHERE codigo = '{}';"
    for codigo, sector in servs.items():
        cur.execute(sql.format(sector, codigo))
