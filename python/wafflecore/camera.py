import math
from time import time
import json

from compute import translate, orientation_direction, orientation_up, rotate, cross_product, unit_vector, product_array_scalar

def test_camera():
    camera = {}
    camera = {"comment" : "fovy is in radians. orientation is right and front", "fovy" : 1.570796, "near" : 0.3, "far" : 1000.0, "resolution" : [300.0, 300.0], "placement" : {"orientation" : {"right" : [1.0, 0.0, 0.0], "front" : [0.0, 1.0, 0.0]}, "position" : [0.0, -10.0, 0.0]}}
    return camera

def camera_aspect(camera):
    aspect = 0.0
    resolution = camera["resolution"]
    aspect = (resolution[0] / resolution[1])
    return aspect

def camera_translate(scale, axis, sign, camera):
    placement = camera["placement"]
    position = placement["position"]
    orientation = placement["orientation"]
    axis = orientation_direction(orientation, axis, sign)
    placement["position"] = translate(position, axis, scale)
    return 

def camera_rotate(scale, axis, sign, camera):
    orientation = camera["placement"]["orientation"]
    front = orientation["front"]
    up = orientation_up(orientation)
    up = unit_vector(up)
    rotate_axis = orientation_direction(orientation, axis, sign)
    front = rotate(front, scale, rotate_axis)
    orientation["front"] = unit_vector(front)
    if (axis == 2.0):
            orientation["right"] = cross_product(orientation["front"], up)
    return 

