import sys
import os

from state import new_state

_devnull = None
_state = None

def get_state(filename=None):
    global _state
    if _state is None:
        with open('settings.json') as f:
            settings = json.loads(f.read())
            _state = new_state(settings)
    return _state

def record(string):
    global _devnull
    if _devnull is None:
        _devnull = open(os.devnull, 'w')
    #sys.stdout = sys.__stdout__
    print string
    #sys.stdout = _devnull
