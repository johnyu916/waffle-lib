import json
from plugins.jsonsyrup import SyrupEncoder
import math
import os.path
from random import random
from time import time
import numpy

from wafflecore.compute import array_scaled, sum_arrays, sum_arrays_3, subtract_arrays_3, point_farthest, time_point_plane, is_overlap_cuboids, matrix_identity, axis_signs_visible, vector_axis_sign, vectors_component, vectors_component_unit, face_overlap, cuboid_new, cuboid_cached_new, bounds_cuboids, farthest_axis_sign, vector_axis_sign
from wafflecore.thing import thing_set_position

def collisions(things, delta):
    for thing in things:
            bounds = thing["bounds"]
            if (bounds == None):
                        continue
            bump_thing(thing, things, delta)
    return 

def position_delta(thing, dt):
    dp = []
    force = thing["force"]
    accel = array_scaled(force, (1.0 / thing["mass"]))
    accel = array_scaled(thing["force"], (1.0 / thing["mass"]))
    velocity_i = thing["velocity"]
    velocity_f = sum_arrays(array_scaled(accel, dt), velocity_i)
    velocity_avg = array_scaled(sum_arrays(velocity_f, velocity_i), (1.0 / 2.0))
    thing["velocity"] = velocity_f
    dp = array_scaled(velocity_avg, dt)
    return dp

def bump_thing(thing, others, dt):
    velocity_i = thing["velocity"]
    thing["collisions"] = []
    thing["dp"] = [0.0, 0.0, 0.0]
    dp = position_delta(thing, dt)
    thing["dv"] = subtract_arrays_3(thing["velocity"], velocity_i)
    if (((dp[0] == 0.0) and (dp[1] == 0.0)) and (dp[2] == 0.0)):
            return 
    bounds = thing["world_bounds"]
    position = bounds["position"]
    position_f = sum_arrays(position, dp)
    crash_position, hit_thing, hit_normal = crash_things(thing["id"], position, position_f, bounds["size"], bounds["max"], others)
    crash_delta = subtract_arrays_3(crash_position, position)
    if (((crash_delta[0] == 0.0) and (crash_delta[1] == 0.0)) and (crash_delta[2] == 0.0)):
            return 
    if (hit_thing != None):
            collision = {"thing" : hit_thing, "normal" : hit_normal}
            thing["collisions"].append(collision)
            thing["velocity"] = [0.0, 0.0, 0.0]
            thing["dv"] = subtract_arrays_3(thing["velocity"], velocity_i)
    thing["force"] = [0.0, 0.0, 0.0]
    last = sum_arrays(thing["position"], crash_delta)
    thing_set_position(thing, [last[0], last[1], last[2]])
    thing["dp"] = crash_delta
    return 

def touching_all(state):
    game = state["game"]
    moving = [game["pacman"]]
    moving.extend(game["enemies"])
    for thing in moving:
            thing["touching"] = []
    for one in moving:
            touch_thing(one, [])
    return 

def touch_thing(thing, others):
    thing["touching"] = []
    thing_bounds = thing["world_bounds"]
    position = thing_bounds["position"]
    size = thing_bounds["size"]
    for two in others:
            if (two["id"] == thing["id"]):
                        continue
            yes, normals = touching_two(position, size, thing_bounds["max"], two)
            if yes:
                        touch = {"thing" : two, "normals" : normals}
                        thing["touching"].append(touch)
    return 

def overlap_bounds_thing(position, size, max, thing):
    hit_thing = {}
    hit_thing = None
    thing_bounds = thing["world_bounds"]
    overlap = is_overlap_cuboids(position, size, max, thing_bounds["position"], thing_bounds["size"], thing_bounds["max"])
    if (overlap == False):
            return hit_thing
    if (len(thing["children"]) > 0.0):
            for child in thing["children"]:
                        child_hit_thing = overlap_bounds_thing(position, size, max, child)
                        if (child_hit_thing != None):
                                        hit_thing = child_hit_thing
                                        return hit_thing
    else:
            hit_thing = thing
    return hit_thing

def touching_one(one, two):
    yes = False
    normals = []
    one_bounds = one["world_bounds"]
    if (len(one["children"]) > 0.0):
            yes, normals = touching_two(one_bounds["position"], one_bounds["size"], two)
            if (yes == False):
                        return yes, normals
            for child in one["children"]:
                        child_yes, child_normals = touching_one(child, two)
                        if child_yes:
                                        yes = True
                                        normals.extend(child_normals)
    else:
            yes, normals = touching_two(one_bounds["position"], one_bounds["size"], two)
    return yes, normals

def touching_two(one_position, one_size, one_max, two):
    yes = False
    normals = []
    two_bounds = two["world_bounds"]
    axis, sign = face_overlap(one_position, one_size, one_max, two_bounds["position"], two_bounds["size"], two_bounds["max"])
    if (len(two["children"]) > 0.0):
            if (axis == None):
                        if (is_overlap_cuboids(one_position, one_size, one_max, two_bounds["position"], two_bounds["size"], two_bounds["max"]) == False):
                                        return yes, normals
            for child in two["children"]:
                        child_yes, child_normals = touching_two(one_position, one_size, one_max, child)
                        if child_yes:
                                        yes = True
                                        normals.extend(child_normals)
    else:
            if (axis != None):
                        yes = True
                        normals.append(vector_axis_sign(axis, sign))
    return yes, normals

def crash_things(thing_id, position_i, position_f, size, max, things):
    final = []
    hit_thing = {}
    hit_normal = []
    delta = subtract_arrays_3(position_f, position_i)
    delta_inv = array_scaled(delta, -1.0)
    peak = point_farthest(position_i, max, delta)
    e_position, e_size = bounds_cuboids([cuboid_new(position_i, size), cuboid_new(position_f, size)])
    extent = cuboid_cached_new(e_position, e_size)
    min_time = 1.0
    hit_thing = None
    for thing in things:
            if (thing["id"] == thing_id):
                        continue
            is_hit, thing_min_time, thing_hit_normal = crash_one(delta, delta_inv, position_i, size, peak, extent, thing)
            if is_hit:
                        if (thing_min_time < min_time):
                                        min_time = thing_min_time
                                        hit_thing = thing
                                        hit_normal = thing_hit_normal
    scale = array_scaled(delta, min_time)
    final = sum_arrays(position_i, scale)
    return final, hit_thing, hit_normal

def crash_one(delta, delta_inv, position_i, size, peak, extent, thing):
    is_hit = False
    min_time = 0.0
    hit_normal = []
    is_hit = False
    min_time = 1.0
    bounds = thing["world_bounds"]
    if (len(thing["children"]) > 0.0):
            if (is_overlap_cuboids(extent["position"], extent["size"], extent["max"], bounds["position"], bounds["size"], bounds["max"]) == False):
                        return is_hit, min_time, hit_normal
            for child in thing["children"]:
                        child_is_hit, crash_time, child_hit_normal = crash_one(delta, delta_inv, position_i, size, peak, extent, child)
                        if child_is_hit:
                                        if (crash_time < min_time):
                                                            min_time = crash_time
                                                            is_hit = True
                                                            hit_normal = child_hit_normal
    else:
            is_hit, crash_time, hit_normal = crash_bounds(position_i, size, peak, delta, bounds)
            if is_hit:
                        if (crash_time < min_time):
                                        min_time = crash_time
    return is_hit, min_time, hit_normal

def crash_bounds(position_i, size, peak, delta, bounds):
    is_hit = False
    crash_time = 0.0
    hit_normal = []
    dest_point = bounds["position"]
    dest_size = bounds["size"]
    for i in range(3):
            magnitude = delta[int(i)]
            if (magnitude == 0.0):
                        continue
            sign = 0.0
            if (magnitude > 0.0):
                        sign = 1.0
            b_peak = farthest_axis_sign(dest_point, bounds["max"], i, (1.0 - sign))
            crash_time = ((b_peak - peak[int(i)]) / magnitude)
            if ((crash_time >= 0.0) and (crash_time < 1.0)):
                        if (magnitude > 0.0):
                                        test = (b_peak + 0.5)
                        else:
                                        test = (b_peak - 0.5)
                        test_time = ((test - peak[int(i)]) / magnitude)
                        test_position = sum_arrays(position_i, array_scaled(delta, test_time))
                        test_max = sum_arrays_3(test_position, size)
                        if is_overlap_cuboids(test_position, size, test_max, dest_point, dest_size, bounds["max"]):
                                        crash_time = crash_time
                                        is_hit = True
                                        hit_normal = vector_axis_sign(i, sign)
                                        break
    return is_hit, crash_time, hit_normal

def some_other():
    vectors = vectors_component(delta)
    unit_vectors = vectors_component_unit(delta)
    for i in range(int(len(vectors))):
            vector = vectors[int(i)]
            unit_vector = unit_vectors[int(i)]
            vector_inv = array_scaled(vector, -1.0)
            child_start = point_farthest(position, max, vector_inv)
            crash_time = time_denorm_point_plane(peak, child_start, vector)
            if ((crash_time >= 0.0) and (crash_time < 1.0)):
                        child_end = sum_arrays(child_start, unit_vector)
                        end_time = time_denorm_point_plane(peak, child_end, vector)
                        if (crash_time == end_time):
                                        print json.dumps(["Error crash_bounds crash_time same as end_time", child_start, child_end], cls=SyrupEncoder)
                        elif (crash_time > end_time):
                                        print json.dumps(["Error end_time greater than crash_time", crash_time, end_time], cls=SyrupEncoder)
                        else:
                                        test_time = ((crash_time + end_time) / 2.0)
                                        test_position = sum_arrays(position_i, array_scaled(delta, test_time))
                                        test_max = sum_arrays_3(test_position, size)
                                        if is_overlap_cuboids(test_position, size, test_max, dest_point, dest_size, bounds["max"]):
                                                            crash_time = crash_time
                                                            is_hit = True
                                                            hit_normal = unit_vector
                                                            break
    return 

