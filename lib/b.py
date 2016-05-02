# b.py, smd/lib/

import datetime

def make_last_update():
    now = datetime.datetime.today().utcnow()
    out = now.isoformat() + 'Z'
    return out

# end b.py


