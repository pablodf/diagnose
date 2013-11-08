# -*- coding: latin-1 -*-

import pymysql
from spiutils.utils import echo

def get_id():
    while 1:
        e = raw_input(echo('Número de documento: '))
        if e == '':
            return None
        if e.isdigit():
            e = int(e)
            break
    return e

def get_record(cur, e, detail=0):
    if detail == 0:
        sql = 'SELECT * FROM personas WHERE nro_doc = {0};'
    elif detail == 1:
        sql = 'SELECT DISTINCT p.id_persona, tipo_doc, nro_doc, '
              'apellido, nombre, sexo, dom_calle, dom_nro, fecha_nac, '
              'origen_info, nom_efector, nom_red_efector FROM personas p '
              'JOIN hc_personas h ON p.id_persona = h.id_persona '
              'JOIN efectores e ON h.id_efector = e.id_efector '
              'JOIN localidades l ON p.id_localidad = l.id_localidad '
              'JOIN origen_info o ON p.id_origen_info = o.id_origen_info '
              'WHERE p.id_persona = {0};'
    try:
        cur.execute(sql.format(e))
        er = cur.fetchall()
        return er
    except:
        return []

PERSONA0 = '[{id_persona:8}] {apellido}, {nombre} - {tipo_doc} {nro_doc} - FN: {fecha_nac}'
PERSONA1 = '''{apellido}, {nombre}
{tipo_doc} {nro_doc}
Sexo: {sexo}
Fecha nac.: {fecha_nac}
Domicilio: {dom_calle} {dom_nro}
{localidad}, {provincia}, {pais}
ID: {id_persona}
'''
PERSONAHC = '''{nom_efector} ({nom_red_efector}) - {origen_info}'''


def show_detail(p):
    print PERSONA1.format(**p)

def show_detail_more(p):
    print PERSONAHC.format(**p)
