from diagnosedump import diagnosedump
from pydiag.utils import waitnquit

dd = diagnosedump.DiagnoseDump(cfgfilename='diagnosedump.cfg')
dd.dump()

waitnquit(0)