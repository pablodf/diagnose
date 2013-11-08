# -*- coding: latin-1 -*-

import pymysql
from pydiag import opciones
from spiutils.utils import echo

def get_conn_cursor(server='localhost', db='diagnose', port=3306):
    try:
        conn = pymysql.connect(host=server, port=port, user='gestion_', passwd='GESTION_77', db=db)
    except:
        return None
    else:
        try:
            cur = conn.cursor(pymysql.cursors.DictCursor)
        except:
            return None
        else:
            return conn, cur

def get_host():
    op = opciones.diagnose_opciones()
    if not op:
        import re
        print echo('No se pudieron leer las opciones de conexión de Diagnose.')
        while 1:
            ip = raw_input(echo('Escriba la dirección IP del servidor de Diagnose:')).strip().lower()
            if ip == '':
                return None
            if ip == 'localhost':
                return ip
            try:
                ipparts = [int(p) for p in ip.split('.')]
            except ValueError:
                continue
            if len(ipparts) == 4:
                if len(filter(lambda x: (x >= 0 and x < 256), ipparts)) == 4:
                    break
        return ip
    else:
        return op['server']
