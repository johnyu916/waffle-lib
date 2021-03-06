import json
from plugins.jsonsyrup import SyrupEncoder
import math
import os.path
from random import random
from time import time
import numpy

from compute import axis_signs_visible, intersect_ray_cuboid_face, magnitude_vector, subtract_arrays, cuboid_transformed, cuboid_new, cuboid_cached_new, matrix_identity, product_matrices, matrix_placement, new_id, filename_type
from standard import array_in_string, copy_object

def thing_new(id, type, position, rotates, children, geometry, bounds):
    thing = {}
    thing = {"id" : id, "type" : type, "position" : position, "velocity" : [0.0, 0.0, 0.0], "rotates" : rotates, "children" : children, "geometry" : geometry, "bounds" : bounds, "matrix" : matrix_identity(), "world_bounds" : None, "mass" : 1.0, "force" : [0.0, 0.0, 0.0], "animate_start" : 0.0}
    return thing

def thing_set_position(thing, position):
    thing["position"] = position
    thing_set_world_bounds(thing, thing["matrix"])
    return 

def thing_set_position_x(thing, x):
    thing["position"][0] = x
    thing_set_world_bounds(thing, thing["matrix"])
    return 

def thing_set_position_y(thing, y):
    thing["position"][1] = y
    thing_set_world_bounds(thing, thing["matrix"])
    return 

def thing_set_position_z(thing, z):
    thing["position"][2] = z
    thing_set_world_bounds(thing, thing["matrix"])
    return 

def thing_blank(id, type):
    thing = {}
    thing = thing_new(id, type, [0.0, 0.0, 0.0], [], [], None, None)
    return thing

def thing_copy(thing, things):
    new_thing = {}
    for key in thing.keys():
            value = thing[key]
            if (key == "geometry"):
                        new_thing["geometry"] = value
            elif (key == "children"):
                        new_children = []
                        for child in value:
                                        child_thing = things[child["name"]]
                                        new_child = thing_copy(child_thing, things)
                                        new_children.append(new_child)
                        new_thing["children"] = new_children
            else:
                        new_thing[key] = copy_object(value)
    return new_thing

def thing_set_children(thing, things):
    new_children = []
    for child in thing["children"]:
            child_thing = things[child["name"]]
            new_children.append(thing_copy(child_thing, things))
    thing["children"] = new_children
    return 

def thing_set_world_bounds(thing, offset):
    thing["matrix"] = offset
    matrix = matrix_placement(thing["position"], thing["rotates"])
    offset = product_matrices(offset, matrix)
    bounds = thing["bounds"]
    if (bounds != None):
            position, size = cuboid_transformed(offset, bounds["position"], bounds["size"])
            thing["world_bounds"] = cuboid_cached_new(position, size)
            for child in thing["children"]:
                        thing_set_world_bounds(child, offset)
    return 

def thing_get_cuboids_unused(thing):
    cuboids = []
    cuboids = []
    if (len(thing["children"]) > 0.0):
            for child in thing["children"]:
                        if (child["dpdt"] == None):
                                        child["dpdt"] = thing["dpdt"]
                        cuboids.extend(thing_get_cuboids_unused(child))
    else:
            p = thing["world_bounds"]["position"]
            v = thing["dpdt"]
            for cube in thing["cuboids"]:
                        new = [cube[0], cube[1], cube[2], cube[3], cube[4], cube[5], cube[6], (cube[7] + p[0]), (cube[8] + p[1]), (cube[9] + p[2]), v[0], v[1], v[2]]
                        cuboids.append(new)
    return cuboids

def thing_read(state, filename):
    thing = []
    text = None
    with open("/".join([state["things_dir"], filename])) as f:
        text = f.read()
    name, ext = filename_type(filename)
    map = json.loads(text)
    children = []
    geometry = None
    if array_in_string(map.keys(), "children_names"):
            child_names = map["children_names"]
            for child_name in child_names:
                        child = {"name" : child_name}
                        children.append(child)
    else:
            geometry_name = map["geometry_name"]
            geometry = state["geometries"][geometry_name]
    thing = thing_new(new_id(state), "", [0.0, 0.0, 0.0], [], children, geometry, None)
    thing.update(map)
    if (array_in_string(thing.keys(), "name") == False):
            thing["name"] = name
    return thing

def thing_load(state, name):
    thing = {}
    text = None
    with open("/".join([state["things_dir"], name])) as f:
        text = f.read()
    map = json.loads(text)
    children = []
    geometry = None
    if array_in_string(map.keys(), "children_names"):
            child_names = map["children_names"]
            for child_name in child_names:
                        child = thing_load(state, child_name)
                        children.append(child)
    else:
            geometry_name = map["geometry_names"][int(map["geometry_index"])]
            geometry = state["geometries"][geometry_name]
    thing = thing_new(new_id(state), "", [0.0, 0.0, 0.0], [], children, geometry, None)
    thing.update(map)
    return thing

def intersect_ray_bounds_unused(origin, direction, thing, faces, offset):
    hit_thing = {}
    hit_face = {}
    hit_point = []
    hit_point = None
    matrix = matrix_placement(thing["position"], thing["rotates"])
    new_offset = product_matrices(offset, matrix)
    new_position, new_size = cuboid_transformed(new_offset, thing["bounds"]["position"], bounds["size"])
    for face in faces:
            hit_point = intersect_ray_cuboid_face(origin, direction, thing["bounds"]["position"], thing["bounds"]["size"], face["axis"], face["sign"])
            if (hit_point != None):
                        hit_thing = thing
                        hit_face = face
                        break
    if (hit_point == None):
            hit_thing = None
            return hit_thing, hit_face, hit_point
    else:
            if (len(thing["cubes"]) == 0.0):
                        for child in thing["children"]:
                                        hit_thing, hit_face, hit_point = intersect_ray_bounds(origin, direction, child, faces)
                                        if (hit_thing != None):
                                                            return hit_thing, hit_face, hit_point
                        hit_thing = None
                        return hit_thing, hit_face, hit_point
            else:
                        return hit_thing, hit_face, hit_point
    return hit_thing, hit_face, hit_point

def intersect_ray_thing(origin, direction, thing):
    hit_thing = {}
    hit_face = {}
    hit_offset = []
    hit_distance = 0.0
    hit_thing = None
    faces = axis_signs_visible(direction)
    hit_thing, hit_face, hit_offset, hit_distance = intersect_ray_thing_faces(origin, direction, thing, matrix_identity(), faces)
    return hit_thing, hit_face, hit_offset, hit_distance

def intersect_ray_thing_faces(origin, direction, thing, offset, faces):
    hit_thing = {}
    hit_face = {}
    hit_offset = []
    min_distance = 0.0
    hit_thing = None
    min_distance = 0.0
    matrix = matrix_placement(thing["position"], thing["rotates"])
    new_offset = product_matrices(offset, matrix)
    if (thing["bounds"] == None):
            for child in thing["children"]:
                        child_hit_thing, child_hit_face, child_hit_offset, child_min_distance = intersect_ray_thing_faces(origin, direction, child, new_offset, faces)
                        if (child_hit_thing != None):
                                        if (hit_thing == None):
                                                            hit_thing = child_hit_thing
                                                            hit_face = child_hit_face
                                                            min_distance = child_min_distance
                                                            hit_offset = child_hit_offset
                                        else:
                                                            if (child_min_distance < min_distance):
                                                                                    hit_thing = child_hit_thing
                                                                                    hit_face = child_hit_face
                                                                                    min_distance = child_min_distance
                                                                                    hit_offset = child_hit_offset
    else:
            bounds = thing["bounds"]
            new_position, new_size = cuboid_transformed(new_offset, bounds["position"], bounds["size"])
            for face in faces:
                        intersect_point = intersect_ray_cuboid_face(origin, direction, new_position, new_size, face["axis"], face["sign"])
                        if (intersect_point != None):
                                        min_distance = magnitude_vector(subtract_arrays(intersect_point, origin))
                                        hit_thing = thing
                                        hit_face = face
                                        hit_offset = new_offset
                                        return hit_thing, hit_face, hit_offset, min_distance
    return hit_thing, hit_face, hit_offset, min_distance

