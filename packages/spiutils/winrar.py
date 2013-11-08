from os.path import join, isfile, dirname
from os import environ


def find_winrar():
    import _winreg
    try:
        h = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
        h = _winreg.OpenKey(h, r'SOFTWARE\WinRAR')
        v = _winreg.QueryValueEx(h, 'exe32')
        if v and len(v) == 2 and v[1] == _winreg.REG_SZ:
            return v[0]
    except WindowsError:
        return None

def find_rar_exe():
    possible = []
    winrar_exe = find_winrar()
    if winrar_exe:
        possible += [
            join(dirname(winrar_exe), 'rar.exe'),
            join(dirname(winrar_exe), 'unrar.exe')
            ]
    if 'ProgramFiles' in environ:
        possible += [
            join(environ['ProgramFiles'], 'WinRAR', 'rar.exe'),
            join(environ['ProgramFiles'], 'UnRAR', 'unrar.exe')
            ]
    for exe in possible:
        if isfile(exe):
            return exe
