import json
import math
import os.path
from time import time

from wafflecore.animation import animate

def idle(state):
    now = time()
    animate(state["animation"], state["world"]["children"][0], state["geometries"], now)
    return 

