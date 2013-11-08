from sys import exit

def echo(s):
    return s.decode('latin1').encode('cp437')

def waitnquit(n=0):
    raw_input(echo('Pulse una tecla para terminar...'))
    exit(n)

def get_dt(prompt, mode='AMD', exitfunc=lambda x: not x):
    import re
    if mode == 'AMD':
        regex = r'(?P<y>20\d\d)-(?P<m>\d{1,2})-(?P<d>\d{1,2})'
    elif mode == 'DMA':
        regex = r'(?P<d>\d{1,2})/(?P<m>\d{1,2})/(?P<y>20\d\d)'
    while True:
        r = raw_input(echo(prompt + '? ')).strip()
        if exitfunc(r):
            return None
        mo = re.match(regex, r)
        if mo:
            y, m, d = [int(x) for x in mo.group('y', 'm', 'd')]
            return '{}-{:02d}-{:02d}'.format(y, m, d)
