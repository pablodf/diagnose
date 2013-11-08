# -*- coding: latin-1 -*-

import os.path
from pydiag import pymy
from pydiag.connection import DiagnoseConnection
from spiutils.utils import echo, waitnquit

host = pymy.get_host()
conn, cur = pymy.get_conn_cursor(host)
cur.execute("SHOW TABLES LIKE 'tConfiguracion';")
if not cur.fetchone():
    print echo('No existe la tabla tConfiguracion.')
else:
    cur.execute("SELECT * FROM tConfiguracion WHERE conf_modulo = 'diagnose' AND conf_clave = 'actualizador' AND conf_atributo = 'path';")
    r = cur.fetchone()
    if not r:
        print echo('No se encuentra ruta de actualización.')
    else:
        path = r['conf_valor']
        print echo('Ruta de actualización: ' + path)
        if os.path.isfile(os.path.join(path, 'diagnose.exe')):
            print echo('Se encontró diagnose.exe en la ruta.')
        else:
            print echo('No se encuentra diagnose.exe en la ruta.')

waitnquit(0)