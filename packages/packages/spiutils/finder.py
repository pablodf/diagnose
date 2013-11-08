import find_mysql
import winrar
import dropbox
import ConfigParser, os
from os.path import join

def find(outfn=None):
    x = dict()
    x['mysqldump'] = find_mysql.find_mysqldump()
    x['mysql'] = find_mysql.find_mysql_binary()
    x['rar'] = winrar.find_rar_exe()
    x['dropbox'] = dbox = dropbox.get_dropbox_folder()
    for root, dirs, names in os.walk(dbox):
        for d in dirs:
            if d == '=dumps=':
                x['dropbox'] = join(root, d)
    if outfn:
        cp = ConfigParser.ConfigParser()
        cp.add_section('location')
        for k, v in x.items():
            if v:
                cp.set('location', k, v)
        with open(outfn, 'w') as f:
            cp.write(f)
    return x