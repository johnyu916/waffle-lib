import json
import math
import os.path
from time import time

from wafflecore.thing import thing_blank
from wafflecore.compute import new_id
from keyboard import new_keyboard

def new_world(state):
    world = {}
    world = thing_blank(new_id(state), "World")
    return world

def new_state(settings):
    state = {}
    state = {"counter" : 1.0, "world" : None, "keyboard" : new_keyboard(), "interface" : None, "animations" : []}
    state.update(settings)
    state["interface"] = thing_blank(new_id(state), "Interface")
    state["world"] = new_world(state)
    return state

