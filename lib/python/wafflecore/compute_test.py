import json
import math
import os.path
from random import random
from time import time

from wafflecore.compute import cuboid_transformed, matrix_placement

def cuboid_transformed_test():
    position = [2.0, 0.0, 3.0]
    rotates = []
    bounds = {"position" : [0.0, 0.0, -1.0], "size" : [14.0, 1.0, 14.0]}
    matrix = matrix_placement(position, rotates)
    position, size = cuboid_transformed(matrix, bounds["position"], bounds["size"])
    print json.dumps(["cuboid_transformed_test", position, size])
    return 

def compute_test():
    cuboid_transformed_test()
    return 

