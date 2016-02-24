import json
from plugins.jsonsyrup import SyrupEncoder
import math
import os.path
from random import random
from time import time
import numpy

from standard import array_in_string, copy_object

def animate(animation, things, geometries, now):
    elapsed_time = (now - animation["time_start"])
    if animation["loop"]:
            elapsed_time = (elapsed_time % animation["duration"])
    action = None
    for frame in animation["actions"]:
            if (elapsed_time > frame["time"]):
                        action = frame
    if (action == None):
            return 
    thing = animation["thing"]
    if array_in_string(action.keys(), "geometry_name"):
            geometry = geometries[action["geometry_name"]]
            thing["geometry"] = geometry
    elif array_in_string(action.keys(), "children_names"):
            new_children = []
            action_children = action["children_names"]
            for name in action_children:
                        new_child = things[name]
                        new_children.append(new_child)
            thing["children"] = new_children
    else:
            for key in action.keys():
                        if (key == "time"):
                                        continue
                        thing[key] = action[key]
    return 

def animation_task(animation, thing, now):
    active = {}
    active = copy_object(animation)
    active["time_start"] = now
    active["thing"] = thing
    return active

