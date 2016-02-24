import json
import math
import os.path
from time import time

from wafflecore.camera import camera_translate, camera_rotate

def new_keyboard():
    keyboard = {}
    KEYS = ["a", "d", "s", "w", "c", "e", "k", "i", "j", "l", "q", "b"]
    return keyboard

def keyboard_on_event(state, key, key_state):
    if (key_state == "KEY_DOWN"):
            keyboard_on_down(state, key, state["camera"])
    else:
            keyboard_on_release(state, key)
    return 

def keyboard_on_release(state, key):
    return 
    return 

def keyboard_on_down(state, key, camera):
    scale = 1.0
    rotate_scale = 0.1
    translate_keys = ["a", "d", "s", "w", "c", "e"]
    axes = [[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0], [2.0, 0.0], [2.0, 1.0]]
    print json.dumps(["camera before", camera["placement"]])
    for i in range(6):
            this_key = translate_keys[int(i)]
            if (key == this_key):
                        camera_translate(scale, axes[int(i)][0], axes[int(i)][1], camera)
                        return 
    axes = [[0.0, 0.0], [0.0, 1.0], [2.0, 1.0], [2.0, 0.0]]
    rotate_keys = ["k", "i", "j", "l"]
    for i in range(4):
            if (key == rotate_keys[int(i)]):
                        camera_rotate(rotate_scale, axes[int(i)][0], axes[int(i)][1], camera)
                        return 
    return 

