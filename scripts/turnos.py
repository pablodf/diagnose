# -*- coding: latin-1 -*-

from pydiag import pymy

# Turnos registrados --> print = '2'
# Turnos presentes --> tipo_turno = '0'
# Turnos ausentes --> tipo_turno = '1'
estado = (
    ('Presentes', 0),
    ('Ausentes', 1)
    )
registro = (
    ('registrados', 2),
    ('no registrados', 0)
    )

EXPR = "SELECT COUNT(*) AS q FROM turnos WHERE dt_baja IS NULL " \
       "AND print = '{}' AND tipo_turno = '{}';"
conn, cur = pymy.get_conn_cursor()
t = dict()
print 'Turnos en sistema:'
for (r, vr) in registro:
    for (e, ve) in estado:
        cur.execute(EXPR.format(vr, ve))
        rec = cur.fetchone()
        print e, r, rec['q']
print

EXPR = "SELECT tipo_turno AS tt, COUNT(*) AS q FROM turnos WHERE dt_baja IS NULL " \
       "AND print = '2' AND DATEDIFF(dt_fecha, dt_pedido) > 0 GROUP BY tt;"
cur.execute(EXPR)
print 'Turnos programados (a un día o más):'.decode('latin-1')
while True:
    rec = cur.fetchone()
    if not rec:
        break
    if rec['tt'] == '0':
        print 'Presentes', rec['q']
    elif rec['tt'] == '1':
        print 'Ausentes', rec['q']
        