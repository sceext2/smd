# smd.py, smd/bin/

import lib.entry as entry

# TODO support --version and --help

# global data
etc = {}
etc['src'] = ''
etc['out'] = ''

def main(argv):
    # TODO more error process
    _p_args(argv)
    
    raw = _read_src(etc['src'])
    
    out = entry.compile(raw)
    
    _write_out(etc['out'], out)
    # done

# process command line arguments
def _p_args(args):
    # TODO more error checks
    rest = args
    while len(rest) > 0:
        one, rest = rest[0], rest[1:]
        if one in ['-o', '--output']:
            etc['out'] = rest[0]
        else:	# default, src file
            etc['src'] = rest[0]
    # done

def _read_src(name):
    with open(name, 'rb') as f:
        blob = f.read()
    text = blob.decode('utf-8')
    return text

def _write_out(name, text):
    blob = text.encode('utf-8')
    with open(name, 'wb') as f:
        f.write(blob)
    # done


# end smd.py


