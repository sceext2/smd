# log.py, smd/lib/

import os, sys

SMD_LOG_PREFIX = 'smd::'

# base print function
def _p(text):
    sys.stdout.write(text)

def _dp(prefix, text):
    out = SMD_LOG_PREFIX + prefix + text
    _p(out)

# exports functions

def w(text):
    _dp('WARNING: ', text)

# TODO more exports

# end log.py


