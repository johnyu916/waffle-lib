import math
from time import time
import json

from compute import cubes_bounds, cuboids_bounds, face_vector, visible_faces, intersect_ray_cuboid_face, magnitude_vector, subtract_arrays, min_cube, cuboid_transformed, cuboid_new, matrix_identity, product_matrices, matrix_placement

def thing_new(id, type, position, rotates, children, geometry):
    thing = {}
    thing = {"id" : id, "type" : type, "position" : position, "rotates" : rotates, "children" : children, "geometry" : geometry, "bounds" : None}
    if (len(geometry) > 0.0):
            thing["bounds"] = bounds_geometry(geometry)
    return thing

def thing_set_bounds_unused(thing, offset):
    matrix = matrix_placement(thing["position"], thing["rotates"])
    new_offset = product_matrices(offset, matrix)
    thing["offset"] = new_offset
    if (len(thing["geometry"]) > 0.0):
            new_position, new_size = cuboid_transformed(new_offset, bounds["position"], bounds["size"])
            thing["bounds"] = cuboid_new(new_position, new_size)
    else:
            cuboids = []
            for child in thing["children"]:
                        thing_set_bounds(child, new_offset)
                        cuboids.append(child["bounds"])
            position, size = cuboids_bounds(cuboids)
            thing["bounds"] = cuboid_new(position, size)
    return 

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
    hit_cube = {}
    hit_face = {}
    hit_distance = 0.0
    hit_thing = None
    faces = visible_faces(direction)
    print json.dumps(faces)
    print json.dumps(["intersect_ray origin ", origin])
    print json.dumps(["intersect_ray direction ", direction])
    hit_cube, hit_face, hit_distance = intersect_ray_thing_faces(origin, direction, thing, matrix_identity(), faces)
    if (hit_cube == None):
            hit_thing = None
    return hit_thing, hit_cube, hit_face, hit_distance

def intersect_ray_thing_faces(origin, direction, thing, offset, faces):
    hit_thing = {}
    hit_face = {}
    min_distance = 0.0
    hit_thing = None
    min_distance = 0.0
    matrix = matrix_placement(thing["position"], thing["rotates"])
    new_offset = product_matrices(offset, matrix)
    if (thing["bounds"] == None):
            for child in thing["chindren"]:
                        child_hit_thing, child_hit_face, child_min_distance = intersect_ray_thing_faces(origin, direction, child, new_offset, faces)
                        if (child_hit_thing != None):
                                        if (hit_thing == None):
                                                            hit_thing = child_hit_thing
                                                            hit_face = child_hit_face
                                                            min_distance = child_min_distance
                                        else:
                                                            if (child_min_distance < min_distance):
                                                                                    hit_thing = child_hit_thing
                                                                                    hit_face = child_hit_face
                                                                                    min_distance = distance
    else:
            bounds = thing["bounds"]
            new_position, new_size = cuboid_transformed(new_offset, bounds["position"], bounds["size"])
            for face in faces:
                        intersect_point = intersect_ray_cuboid_face(origin, direction, new_position, new_size, face["axis"], face["sign"])
                        if (intersect_point != None):
                                        min_distance = magnitude_vector(subtract_arrays(intersect_point, origin))
                                        hit_thing = thing
                                        hit_face = face
                                        return hit_thing, hit_face, min_distance
    return hit_thing, hit_face, min_distance

def collide():
    return 
    return 

