# -*- coding: latin-1 -*-

from pydiag import alertas, pymy, opciones
from spiutils.utils import echo, waitnquit
from spiutils import dropbox
import sys, os
import ConfigParser

def get_cfg():
    cfgfile = 'alertas-q.cfg'
    parser = ConfigParser.ConfigParser()
    if os.path.isfile(cfgfile):
        try:
            f = open(cfgfile, 'r')
            parser.readfp(f)
            return parser.get('log', 'log')
        except:
            pass

def try_(r):
    if r is None:
        sys.exit(1)
    else:
        return r

def main():
    # Leer opciones de Diagnose
    host = try_(pymy.get_host())
    # Conectar con base de datos
    conn, cur = try_(pymy.get_conn_cursor(host))
    # Pedir al usuario el número de alerta
    e = try_(alertas.get_id())
    # Buscar alerta en la base de datos
    er = alertas.get_record(cur, e)
    if er:
        ers = alertas.ALERTA.format(**er)
        print echo(ers)
        raw_input()

        logpath = get_cfg()
        if not logpath:
            logpath = './'
        elif '%DBOX%' in logpath:
            dbox = dropbox.get_dropbox_folder() or './'
            logpath = logpath.replace('%DBOX%', dbox)
        if os.path.isdir(logpath):
            fn = os.path.normpath(os.path.join(logpath, 'alertas.txt'))
            with open(fn, 'w') as f:
                f.write(ers)
                os.startfile(fn)
    else:
        print echo('No se encuentra el número de error'), e
        waitnquit(1)

if __name__ == '__main__':
    main()