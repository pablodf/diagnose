# -*- coding: latin-1 -*-

import zipfile
from os.path import join, isdir, isfile
from os import environ, getcwd, makedirs
from pydiag import opciones
from spiutils import dropbox, sqldump
from ConfigParser import ConfigParser


class DiagnoseConfigError(Exception):
    pass


class DiagnoseConfig:
    def __init__(self, cfgfile='diagnosedump.cfg'):
        if not isfile(cfgfile):
            raise DiagnoseConfigError, 'Configuration file not found.'
        cfg = ConfigParser()
        cfg.read([cfgfile])
        if not cfg.has_section('main'):
            raise DiagnoseConfigError, 'Configuration file is malformed.'
        for (n, v) in cfg.items('main'):
            setattr(self, n, v)
        self.config = cfg


class DiagnoseDumpError(Exception):
    pass


class DiagnoseDump:
    def __init__(self, databases=None, path=None, cfgfilename=None):
        """
        Prepara un volcado de alguna base de datos de Diagnose.

        Dada una lista de bases de datos y una ruta, prepara lo
        necesario para realizar un volcado de cada una de ellas,
        comprimido en formato ZIP, en una carpeta dada por el
        usuario o alguna otra de varias por defecto. Requiere
        que haya un cliente de Diagnose con su archivo de
        configuración apuntando al servidor y que se pueda
        localizar mysqldump.exe. Opcionalmente puede realizar
        el volcado en la carpeta de Dropbox del usuario, si
        existe.
        """
        try:
            # Intenta importar la interfase con Dropbox y obtener
            # la carpeta Dropbox del usuario.
            self.dbox = dropbox.get_dropbox_folder()
        except ImportError:
            self.dbox = None
        # Determina la ruta de almacenamiento del volcado comprimido
        # entre varias alternativas que deberían ser accesibles.
        path2 = None
        cfg = None
        try:
            cfg = DiagnoseConfig(cfgfilename)
            path2 = cfg.dumpinto
            if not databases and cfg.config.has_section('databases'):
                databases = [k for (k, v) in cfg.config.items('databases') if str(v) == '1']
        except DiagnoseConfigError:
            pass
        self.path = path or path2 or self.dbox or environ.get('PUBLIC') or getcwd()
        # Busca el servidor de Diagnose (no chequea el acceso).
        # Si el archivo de configuración no existe o no está bien formado
        # aborta con una excepción.
        user = 'gestion_'
        password = 'GESTION_77'
        try:
            from diagnose import opciones
            o = opciones.diagnose_opciones()
        except ImportError:
            o = dict()
        if o and 'server' in o:
            host = o['server']
        elif cfg and hasattr(cfg, 'host'):
            host = cfg.host
            if hasattr(cfg, 'user') and hasattr(cfg, 'password'):
                user = cfg.user
                password = cfg.password
        else:
            raise DiagnoseDumpError, 'No sé dónde se encuentra el servidor de Diagnose.'
        self.databases = databases or ('diagnose', 'hmi2')
        # Crea el wrapper para mysqldump
        self.mysqldump = sqldump.SQLDump(host=host, user=user, password=password)
        self.config = cfg

    def check(self, path=None):
        if not path:
            path = self.path
        if not isdir(path):
            makedirs(path)

    def dump_db(self, database, tables=None, path=None):
        # Si no se detallan tablas a volcar, ver si hay detalle
        # en la configuración. De lo contrario se volcarán todas
        # las tablas de la base de datos.
        cfg = self.config
        if cfg and not tables and cfg.config.has_section('db-' + database):
            # Por ejemplo:
            #   [db-diagnose]
            #   paciente = 1
            tables = [k for (k, v) in cfg.config.items('db-' + database) if str(v) == '1']
        if not path:
            path = self.path
        self.check()
        print 'Volcando:', database
        dumpfn = self.mysqldump.dump(database, tables)
        zipname = join(self.path, database + '.zip')
        print 'Comprimiendo en', zipname
        with zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(dumpfn, database + '.sql')
        return zipname

    def dump(self, databases=None, path=None):
        if not databases:
            databases = self.databases
        zipnames = dict()
        if not path:
            path = self.path
        for db in databases:
            zipnames[db] = self.dump_db(db, path=path)
        return zipnames