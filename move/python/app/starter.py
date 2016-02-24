import json
import math
import os.path
from time import time

from wafflecore.thing import thing_new
from wafflecore.compute import new_id

def thing_move_read(state):
    thing = {}
    text = None
    with open("/".join([state["things_dir"], state["thing_name"]])) as f:
        text = f.read()
    map = json.loads(text)
    geometry = state["geometries"][map["geometry_name"]]
    thing = thing_new(new_id(state), "Object", map["position"], map["rotates"], [], geometry, map["bounds"])
    return thing

def start(argv, state):
    text = None
    with open("/".join([state["animations_dir"], state["animation_name"]])) as f:
        text = f.read()
    animation = json.loads(text)
    state["animation"] = animation
    geometries = {}
    for action in animation["actions"]:
            if (action["type"] == "vertices"):
                        with open("/".join([state["geometries_dir"], action["geometry_name"]])) as f:
                            text = f.read()
                        geometry = {"vertices" : json.loads(text), "id" : new_id(state)}
                        geometries[action["geometry_name"]] = geometry
    state["geometries"] = geometries
    thing = thing_move_read(state)
    state["world"]["children"].append(thing)
    return 

