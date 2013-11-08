#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, subprocess, tempfile, zipfile
from spiutils.utils import waitnquit

def get_format(fn):
    if zipfile.is_zipfile(fn):
        return 'zip'
    else:
        with open(fn, 'rb') as rarf:
            magic = rarf.read(7)
            if magic == 'Rar!\x1a\x07\x00':
                return 'rar'


if len(sys.argv) < 2:
    print 'Se requiere al menos un parámetro.'
    waitnquit(1)


for fn in sys.argv[1:]:
    if not os.path.isfile(fn):
        print 'El parámetro debe ser un nombre de archivo existente.'
        waitnquit(2)

    fmt = get_format(fn)
    if not fmt:
        print 'El archivo no parece ser un archivo ZIP o RAR.'
        waitnquit(3)

    X = tempfile.mkdtemp()
    if fmt == 'rar':
        r = subprocess.call(['unrar', 'e', '-ep', '-y', fn, '*.sql', X])
        if r != 0:
            print 'Hubo un error en UnRAR.'
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
        print 'Llamando a MySQL para importar', sqlfn
        r = subprocess.call(
            ['mysql', '-uroot', '-pnokia3189', db],
            stdin=sqlf)
        if r == 0:
            print 'MySQL finalizó correctamente.'
        else:
            print 'MySQL finalizó con código de salida', r
        
    sqlf.close()
    print 'Quitando archivo', sqlfn
    os.remove(sqlfn)

waitnquit(0)
