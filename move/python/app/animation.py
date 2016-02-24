import json
import math
import os.path
from time import time


def animate(animation, thing, geometries_map, time):
    if animation["loop"]:
            time = (time % animation["duration"])
    print json.dumps(["in animate", time])
    action = None
    for frame in animation["actions"]:
            if (time > frame["time"]):
                        action = frame
    if (action["type"] == "vertices"):
            print json.dumps(["in animate action ", action["geometry_name"]])
            geometry = geometries_map[action["geometry_name"]]
            thing["geometry"] = geometry
    else:
            for placement in action["placements"]:
                        child = thing["children"][int(placement["index"])]
                        child["rotates"] = placement["rotates"]
    return 

