import math
from time import time
import json

from compute import cubes_bounds, cuboids_bounds, face_vector, visible_faces, intersect_ray_cuboid_face, magnitude_vector, subtract_arrays, min_cube, cuboid_transformed, cuboid_new, matrix_identity, product_matrices, matrix_placement

def thing_new(id, name, type, position, rotates, cubes, children):
    thing = {}
    thing = {"id" : id, "name" : name, "type" : type, "position" : position, "rotates" : rotates, "children" : children, "cubes" : cubes, "offset" : None, "bounds" : None}
    return thing

def min_thing(thing):
    to_save = {}
    min_children = []
    for child in thing["children"]:
            min_children.append(min_thing(child))
    min_cubes = []
    for cube in thing["cubes"]:
            min_cubes.append(min_cube(cube))
    to_save = {"name" : thing["name"], "children" : min_children, "cubes" : min_cubes, "type" : thing["type"], "bounds" : None}
    return to_save

def thing_set_bounds(thing, offset):
    matrix = matrix_placement(thing["position"], thing["rotates"])
    new_offset = product_matrices(offset, matrix)
    thing["offset"] = new_offset
    if (len(thing["cubes"]) > 0.0):
            bounds = cubes_bounds(thing["cubes"])
            new_position, new_size = cuboid_transformed(new_offset, bounds["position"], bounds["size"])
            thing["bounds"] = cuboid_new(new_position, new_size, [0.0, 0.0, 0.0, 0.0])
    else:
            cuboids = []
            for child in thing["children"]:
                        thing_set_bounds(child, new_offset)
                        cuboids.append(child["bounds"])
            position, size = cuboids_bounds(cuboids)
            thing["bounds"] = cuboid_new(position, size, [0.0, 0.0, 0.0, 0.0])
    return 

def intersect_ray_bounds(origin, direction, thing, faces):
    hit_thing = {}
    hit_face = {}
    hit_point = []
    hit_point = None
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
    hit_cube = {}
    hit_face = {}
    hit_distance = 0.0
    hit_thing = None
    faces = visible_faces(direction)
    print json.dumps(faces)
    print json.dumps(["intersect_ray origin ", origin])
    print json.dumps(["intersect_ray direction ", direction])
    if (thing["bounds"] == None):
            thing_set_bounds(thing, matrix_identity())
            print json.dumps(["thing_bounds ", thing["bounds"]])
    hit_thing, bounds_face, hit_point = intersect_ray_bounds(origin, direction, thing, faces)
    if (hit_thing == None):
            print json.dumps(["intersect_ray_thing null "])
            return hit_thing, hit_cube, hit_face, hit_distance
    print json.dumps(["intersect_ray point ", hit_point, bounds_face])
    hit_cube, hit_face, hit_distance = intersect_ray_cubes(origin, direction, hit_thing["cubes"], hit_thing["offset"], faces)
    if (hit_cube == None):
            hit_thing = None
    return hit_thing, hit_cube, hit_face, hit_distance

def intersect_ray_cubes(origin, direction, cubes, offset, faces):
    hit_cube = {}
    hit_face = {}
    min_distance = 0.0
    if (len(cubes) == 0.0):
            hit_cube = None
            return hit_cube, hit_face, min_distance
    first = cubes[0]
    size = first["size"]
    sizes = [size, size, size]
    hit_cube = None
    min_distance = 0.0
    distance = 0.0
    for cube in cubes:
            new_position, new_size = cuboid_transformed(offset, cube["position"], sizes)
            for face in faces:
                        intersect_point = intersect_ray_cuboid_face(origin, direction, new_position, new_size, face["axis"], face["sign"])
                        if (intersect_point != None):
                                        distance = magnitude_vector(subtract_arrays(intersect_point, origin))
                                        if (hit_cube == None):
                                                            hit_cube = cube
                                                            hit_face = face
                                                            min_distance = distance
                                        else:
                                                            if (distance < min_distance):
                                                                                    hit_cube = cube
                                                                                    hit_face = face
                                                                                    min_distance = distance
    return hit_cube, hit_face, min_distance

def collide():
    return 
    return 

