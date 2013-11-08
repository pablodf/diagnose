from spiutils import winrar
from subprocess import call
from os.path import isfile, isdir, basename
from shutil import rmtree
import tempfile

class RarError(Exception):
    pass

RAR_SIGNATURE = 'Rar!\x1a\x07\x00\xcf'

class RarFile:
    """Wrapper around RAR.EXE.

    A RarFile object provides a minimal interface around a RAR archive file.
    Given a filename, it tests whether it is a RAR file and checks for the
    existence of WinRAR's RAR.EXE. It is intended as a parallel to the
    _zipfile_ standard module.  
    """
    def __init__(self, filename, test=True, find_exe=True):
        if isinstance(filename, (str, unicode)) and isfile(filename):
            self.filename = filename
        else:
            raise IOError, 'First argument must be an existing filename.'
        with open(self.filename, 'rb') as rarf:
            if bytes(rarf.read(8)) != RAR_SIGNATURE:
                raise RarError, 'RAR archive signature not found.'
        if find_exe:
            self.find_exe()
        if test:
            self.test()
        self.lastdest = None

    def find_exe(self):
        """Check for the existence of RAR.EXE.

        Since Python is not capable of directly manipulating RAR files,
        commands are to be passed to RAR.EXE. As a first approximation
        the Windows Registry is searched for a WinRAR installation. If
        found, the location of RAR.EXE (the command-line client) is
        stored for future use.
        """
        exe = winrar.find_rar_exe()
        if exe:
            self.exe = exe
            self.exename = basename(exe)
        else:
            raise IOError, 'No RAR executable found.'

    def test(self):
        """Test the file for format and errors.

        RAR.EXE is called to test the file. The return value is
        passed along. A non-zero return value of zero signals an error.
        """
        return call([self.exe, 't', self.filename])

    def decompress(self, command='x', params=None, filenames='*', dest=None):
        """Decompress some or all files inside the archive into a destination.

        This method is a wrapper around RAR's decompression commands.
        If command == 'x', then RAR will extract files with full paths.
        If command == 'e', files will be extracted on the working directory.
        If no destination is given, the archive will be decompressed into
        a temporary folder, which will be saved in the lastdest attribute.
        Giving a non-existing destination is an error.
        """
        if command not in ('e', 'x'):
            raise RarError, 'Allowed decompression commands are "e" and "x".'
        if not params:
            params = []
        if dest is None:
            dest = tempfile.mkdtemp()
            self.lastdest = dest
        if not isdir(dest):
            raise IOError, 'Destination does not exist: ' + dest
        if not dest.endswith('\\'):
            dest += '\\'
        rarp = call([self.exe, command] + params + [self.filename, filenames, dest])
        if rarp != 0:
            raise RarError, 'RAR error during decompression, return code: ' + rarp
        else:
            return dest

    def get_filelist(self, detailed=False):
        """Get a list of the archive's contents.

        Call RAR.EXE to get a list of the archive file's contents. The output
        is piped into a temporary file, read on the fly and discarded. A list
        of the filenames is returned.
        """
        command = (detailed and 'v' or 'l') + 'b'
        # No "technical" option is allowed (RAR vt / RAR lt)
        with tempfile.SpooledTemporaryFile() as tempf:
            rarp = call([self.exe, command, self.filename], stdout=tempf)
            tempf.seek(0)
            if rarp == 0:
                self.filelist = [line.strip() for line in tempf]
                return self.filelist

    def cleanup(self):
        if self.lastdest:
            shutil.rmtree(self.lastdest)