# -*- coding: latin-1 -*-

from spiutils.utils import echo

def get_id():
    while 1:
        e = raw_input(echo('Número de error: '))
        if e == '':
            return None
        if e.isdigit():
            e = int(e)
            break
    return e

def get_record(cur, e):
    try:
        cur.execute('SELECT * FROM alertas WHERE id = {0};'.format(e))
        er = cur.fetchone()
        return er
    except:
        return None

ALERTA = '''Id: {id}
Descripción: {Desc_e}
Evento: {Evento}
Formulario: {Formulario}
Puesto: {PuestoTrabajo}
Nro. error: {nro_e}
Fecha/hora: {dt_created}'''