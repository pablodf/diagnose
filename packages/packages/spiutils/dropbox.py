import os
import shutil
from base64 import b64decode
from zipfile import ZipFile, ZIP_DEFLATED

def get_dropbox_folder():
    if 'APPDATA' in os.environ:
        fn = os.path.join(os.environ['APPDATA'], 'Dropbox', 'host.db')
        if os.path.isfile(fn):
            with open(fn, 'rb') as f:
                f.readline()
                s = f.readline()
                dropboxdir = b64decode(s)
                if os.path.isdir(dropboxdir):
                    return dropboxdir

def copy(fn, subfolder='', zip=True, timestamp=False, move=False):
    dst = get_dropbox_folder()
    if dst and os.path.isfile(fn):
        if zip:
            name, ext = os.path.splitext(fn)
            if timestamp:
                import time
                name = name + time.strftime('-%Y%m%d-%H%M%S')
            z = ZipFile(name + '.zip', 'w', ZIP_DEFLATED)
            z.write(fn, os.path.basename(fn))
            z.close()
            fn = name + '.zip'
        func = move and shutil.move or shutil.copy
        func(fn, os.path.join(dst, subfolder))
