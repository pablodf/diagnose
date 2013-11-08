from os import environ, getcwd
from os.path import isfile, join

def _PATH():
    return environ['PATH'].split(';')

def isinPATH(name, iswhat=isfile, cwd=True):
    PATH = _PATH()
    if cwd:
        PATH.append(getcwd())
    for path in PATH:
        if iswhat(join(path, name)):
            return join(path, name)
