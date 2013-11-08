# -*- coding: latin-1 -*-

import sys, os, subprocess, tempfile, zipfile

def echo(s):
    return s.decode('latin1').encode('cp437')

def quit(n):
    raw_input(echo('Pulse una tecla para terminar...'))
    sys.exit(n)

def findfile(filename, path):
    for root, dirs, names in os.walk(path):
        if filename in names:
            return os.path.join(root, filename)
    return None

def findfileinPATH(filename):
    for path in os.environ['PATH'].split(';'):
        fn = os.path.join(path, filename)
        if os.path.isfile(fn):
            return fn
    return None

print echo('Buscando mysqldump.exe en el PATH...')
exe = findfileinPATH('mysqldump.exe')
if exe is None:
    print echo('Buscando mysqldump.exe...')
    exe = findfile('mysqldump.exe', os.environ['ProgramFiles'])
    if exe is None:
        print echo('No se encontró mysqldump.exe.')
        quit(1)

db = raw_input(echo('Base de datos: ')).strip()
if db == '':
    print echo('Se canceló el proceso.')
    quit(1)

tempd = tempfile.mkdtemp()
tempfn = os.path.join(tempd, db + '.sql')

with open(tempfn, 'w') as sqlf:
    print echo('Abierto {} para escritura.'.format(tempfn))
    print echo('Llamando a mysqldump...')
    p_my = subprocess.Popen(
        [exe, '-ugestion_', '-pGESTION_77', db],
        stdout=sqlf)
    ret = p_my.wait()
    if ret == 0:
        print echo('mysqldump finalizó correctamente.')
    else:
        print echo('mysqldump finalizó con código de salida'), ret
        quit(ret)

basefn = os.path.basename(tempfn)
zfn = os.path.join(tempd, os.path.splitext(basefn)[0] + '.zip')
with zipfile.ZipFile(zfn, 'w', zipfile.ZIP_DEFLATED) as zf:
    print echo('Comprimiendo en {}...'.format(zfn))
    zf.write(tempfn, basefn)
print echo('Se comprimió correctamente el archivo.')
os.startfile(tempd, 'explore') 
quit(0)
