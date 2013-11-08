# -*- coding: latin-1 -*-

import tempfile, webbrowser, time

def maketimestamp(tag='div', class_='timestamp'):
    now = time.strftime('%d/%m/%Y %H:%M:%S')
    if tag:
        tclass = class_ and ' class="{}"'.format(class_) or ''
        return '<{0}{1}>{2}</{0}>'.format(tag, tclass, now)
    else:
        return now

# Enviar datos a un archivo HTML y abrirlo
def print2html(html, data):
    fd, fn = tempfile.mkstemp(suffix='.html', text=True)
    with file(fn, 'w') as outf:
        outf.write(html)
        outf.write('<table id="res">\n'
                   '<thead><tr><th>Frecuencia</th><th>Código CIE-10</th><th>Descripción</th></thead>\n'
                   '<tbody>\n')
        outf.write('</tbody>\n</table>\n' + maketimestamp() + '</body>\n</html>\n')
    webbrowser.open_new_tab('file:///' + fn)

print2html('<h1>Test</h1>', None)
