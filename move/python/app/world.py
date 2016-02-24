import json
import math
import os.path
from time import time

from wafflecore.thing import thing_new
from wafflecore.compute import new_id

def new_world(state):
    world = {}
    world = thing_new(new_id(state), "World", [0.0, 0.0, 0.0], [], [], None)
    return world

