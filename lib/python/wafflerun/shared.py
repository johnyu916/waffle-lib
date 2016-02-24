import sys
import os
import json

from app.state import new_state

_devnull = None
_state = None

def get_state():
    return _state


def set_state(settings_path):
    global _state
    if _state is None:
        with open(settings_path) as f:
            settings = json.loads(f.read())
            _state = new_state(settings)

def record(string):
    global _devnull
    if _devnull is None:
        _devnull = open(os.devnull, 'w')
    #sys.stdout = sys.__stdout__
    print string
    #sys.stdout = _devnull
