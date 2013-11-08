from subprocess import call
import tempfile

with tempfile.SpooledTemporaryFile() as outf:
    r = call(['mysql.exe', '-uroot', '-pnokia3189', '-N', '-t', '-e', 'SELECT * FROM hmi2.versiones;'], stdout=outf)
    outf.seek(0)
    res = outf.readlines()
    versiones = {}
    for line in res:
        if line.startswith('|'):
            fields = [fld.strip() for fld in line.strip().strip('|').split('|')]
            versiones[fields[0]] = fields[1]
    print versiones