# -*- coding: latin-1 -*-

import sys, os, subprocess, tempfile, zipfile
from spiutils import find_mysql
from spiutils.utils import echo, waitnquit

def get_format(fn):
    if zipfile.is_zipfile(fn):
        return 'zip'
    else:
        with open(fn, 'rb') as rarf:
            magic = rarf.read(7)
            if magic == 'Rar!\x1a\x07\x00':
                return 'rar'


X = tempfile.mkdtemp()

if len(sys.argv) < 2:
    print echo('Se requiere al menos un parámetro.')
    waitnquit(1)

fn = sys.argv[1]
if not os.path.isfile(fn):
    print echo('El primer parámetro debe ser un nombre de archivo existente.')
    waitnquit(2)

fmt = get_format(fn)
if not fmt:
    print echo('El archivo no parece ser un archivo ZIP o RAR.')
    waitnquit(3)

mysql_exe = find_mysql.find_mysql_binary('mysql.exe')
if not mysql_exe:
    print echo('No se encuentra mysql.exe.')
    waitnquit(4)

if fmt == 'rar' and 'ProgramFiles' in os.environ:
    rar_exe = os.path.join(os.environ['ProgramFiles'], 'WinRar', 'rar.exe')
    if not os.path.isfile(rar_exe):
        print echo('No se encuentra ejecutable de RAR.')
        waitnquit(5)
    r = subprocess.call([rar_exe, 'e', '-ep', '-y', fn, '*.sql', X])
    if r != 0:
        print echo('Hubo un error en WinRAR.')
        waitnquit(6)
elif fmt == 'zip':
    with zipfile.ZipFile(fn, 'r') as zipf:
        names = [os.path.basename(name)
                 for name in zipf.namelist()
                 if name.endswith('.sql')]
        for name in names:
            zipf.extract(name, X)

fnbase = os.path.basename(fn)
for db in ('diagnose', 'hmi2', 'compras', 'aymara'):
    if fnbase.startswith(db):
        if fnbase[len(db):].startswith('-mini'):
            dbdump = db + '-mini'
        else:
            dbdump = db
        break

fnbase = dbdump + '.sql'
sqlfn = os.path.join(X, fnbase)

with open(sqlfn) as sqlf:
    print echo('Llamando a MySQL para importar'), echo(sqlfn)
    r = subprocess.call(
        [mysql_exe, '--debug-info', '-uroot', '-pnokia3189', db],
        stdin=sqlf)
    if r == 0:
        print echo('MySQL finalizó correctamente.')
    else:
        print echo('MySQL finalizó con código de salida'), r
    
sqlf.close()
print echo('Quitando archivo'), echo(sqlfn)
os.remove(sqlfn)

waitnquit(0)