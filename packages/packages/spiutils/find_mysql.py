# -*- coding: latin-1 -*-

import _winreg
from os.path import join, isfile
from isinpath import isinPATH

def find_mysql_in_registry():
    """Find MySQL Server installations in the Windows Registry.

    Connects to the Windows Registry and collects data from
    installations of MySQL Server. No guarantees are given that
    the installations reported are current, functional or to be
    found in the location given in the Registry. Returns a list
    of dictionary objects with keys 'Location' and 'Version'. The
    values are: for 'Location', the folder where the MySQL binaries
    are stored; for 'Version', a version string (actually, according
    to MySQL, a distribution string).

    If you need to find a particular installed version, use
    find_mysql_ver(major, minor).
    """
    try:
        h = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
        h = _winreg.OpenKey(h, r'SOFTWARE\MySQL AB')
    except WindowsError:
        return None
    i = 0
    installations = []
    while True:
        try:
            k = _winreg.EnumKey(h, i)
            if k.startswith('MySQL Server'):
                data = dict()
                h_ = _winreg.OpenKey(h, k)
                for vname in ('Location', 'Version'):
                    v = _winreg.QueryValueEx(h_, vname)
                    if v and len(v) == 2 and v[1] == _winreg.REG_SZ:
                        data[vname] = v[0]
                installations.append(data)
            i += 1
        except WindowsError:
            break
    return installations


def find_mysql_ver(major=None, minor=None):
    """Find an installed version of MySQL Server in Windows.

    Looks for installed versions of MySQL Server in the Windows
    Registry, with a specified major and minor version numbers.
    There are no guarantees that the Registry is current and/or
    correct.
    """
    installations = find_mysql_in_registry()
    for inst in installations:
        ver = inst['Version']
        imajor, iminor, revs = ver.split('.', 2)
        if not major and not minor:
            return inst
        major, minor = str(major or ''), str(minor or '')
        if imajor == major and (not minor or iminor == minor):
            return inst


def find_mysqldump(exe='mysqldump.exe'):
    """Find mysqldump.exe, the MySQL client for database dumping.

    Looks for the MySQL binary mysqldump.exe in several different
    places, starting with the location(s) possibly found in the
    Windows Registry, plus the PATH and the current directory.
    Returns the full path to the file if it is actually present,
    or None otherwise.
    """
    r = find_mysql_in_registry()
    if r:
        for inst in r:
            mypath = inst['Location']
            myname = join(mypath, 'bin', exe)
            if isfile(myname):
                return myname
    else:
        return isinPATH(exe, cwd=True) or None

def find_mysql_binary(exe='mysql.exe'):
    r = find_mysql_in_registry()
    if r:
        for inst in r:
            mypath = inst['Location']
            myname = join(mypath, 'bin', exe)
            if isfile(myname):
                return myname
    else:
        return isinPATH(exe, cwd=True) or None