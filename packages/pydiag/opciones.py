import os, re
from ConfigParser import ConfigParser

pppath = (
    './',
    r'C:\SPI',
    r'D:\SPI',
    'ProgramFiles' in os.environ and os.environ['ProgramFiles'],
    'C:\\',
    'D:\\'
    )

def get_optionfile(filename):
    for x in pppath:
        if os.path.isdir(x):
            oppath = os.path.join(x, 'diagnose', filename)
            if os.path.isfile(oppath):
                return oppath

def get_opciones_dat():
    return get_optionfile('opciones.dat')

def get_hmi2_ini():
    return get_optionfile('hmi2.ini')

def diagnose_opciones():
    fn = get_opciones_dat()
    if fn:
        ops = dict()
        with open(fn, 'r') as f:
            for line in f:
                mo = re.match(r'"(.+?)"\s*,\s*"(.*?)"', line)
                if mo:
                    ops[mo.group(1).strip()] = mo.group(2).strip()
        return ops

def hmi2_opciones():
    fn = get_hmi2_ini()
    if fn:
        ini = ConfigParser()
        if ini.read(fn):
            return dict(ini.items('conexion'))

def diagnose_write(o, v):
    ops = diagnose_opciones()
    if o in ops:
        ops[o] = v
    fn = get_opciones_dat()
    with open(fn, 'w') as f:
        for o in ops:
            f.write('"{0}","{1}"\n'.format(o, ops[o]))

def hmi2_write(s, o, v):
    fn = get_hmi2_ini()
    if fn:
        ini = ConfigParser()
        if ini.read(fn):
            ini.set(s, o, v)
            ini.write(open(fn, 'w'))

if __name__ == '__main__':
    print diagnose_opciones()
    print hmi2_opciones()
