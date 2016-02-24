import json
from plugins.jsonsyrup import SyrupEncoder
import math
import os.path
from random import random
from time import time
import numpy


def array_in_string(stuff, key):
    yes = False
    for element in stuff:
            if (element == key):
                        yes = True
                        return yes
    return yes

def copy_object(a):
    b = {}
    text = json.dumps(a, cls=SyrupEncoder)
    b = json.loads(text)
    return b

