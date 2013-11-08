from pydiag import opciones, pymy
from pydiag.utils import echo

# Obtener del usuario una fecha en el formato AAAA/MM/DD
def get_dt(prompt, exitfunc=lambda x: not x):
    while True:
        r = raw_input(echo(prompt + '? ')).strip()
        if exitfunc(r):
            return None
        mo = re.match(r'(20\d\d)-(\d{1,2})-(\d{1,2})', r)
        if mo:
            y, m, d = [int(x) for x in mo.group(1, 2, 3)]
            return '{}-{:02d}-{:02d}'.format(y, m, d)

def makesearch(dt0=None, dt1=None):
    # Retornar una sentencia SQL apropiada
    pass

def makehtml(op, dt0=None, dt1=None):
    # Retornar una plantilla HTML (para usar con .format())
    pass
    
def print2html(html, data):
    # Volcar a pantalla o archivo los datos según la plantilla
    pass


def __main__():
    op = opciones.diagnose_opciones()
    if not op:
        print echo('No se encuentran las opciones de conexión. No se puede conectar a la base de datos de Diagnose.')
        exit(1)

    # Búsqueda por fecha
    print echo('Escriba las fechas en formato AAAA-MM-DD para filtrar la búsqueda.\nDeje vacía la pregunta si no desea filtrar por fecha.')
    dt0 = get_dt('Fecha desde')
    dt1 = get_dt('Fecha hasta')

    print 'Conectando a la base de datos...'
    host = pymy.get_host()
    conn, cur = pymy.get_conn_cursor(host)

    sql = makesearch(dt0, dt1)
    print 'Consultando...'
    cur.execute(sql)
    print 'Recuperando datos...'
    data = cur.fetchall()
    print 'Listo.'

    html = makehtml(op, dt0, dt1)
    print2html(html, data)


if __name__ == '__main__':
    __main__()
