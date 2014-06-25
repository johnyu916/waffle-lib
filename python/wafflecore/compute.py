import json
import math
import os.path
from random import random
from time import time


def new_id(state):
    id = ""
    id = json.dumps(state["counter"])
    state["counter"] += 1.0
    return id

def is_extension(filename, ext):
    yes = False
    texts = filename.split(".")
    end = (len(texts) - 1.0)
    if (texts[int(end)] == "json"):
            yes = True
    return yes

def new_placement(orient, position):
    placement = {}
    placement = {"orient" : orient, "position" : position}
    return placement

def new_square(position, size, axis):
    square = {}
    square = {"position" : position, "size" : size, "axis" : axis}
    return square

def rectangle_new(position, size, axis):
    rectangle = {}
    rectangle = {"position" : position, "size" : size, "axis" : axis}
    return rectangle

def rectangle_2d_new(position, size):
    rectangle = {}
    rectangle = {"position" : position, "size" : size}
    return rectangle

def axis_sign_new(axis, sign):
    face = {}
    face = {"axis" : axis, "sign" : sign}
    return face

def cuboid_color_new(position, size, color):
    cuboid = {}
    cuboid = {"position" : position, "size" : size, "color" : color}
    return cuboid

def cuboid_new(position, size):
    cuboid = {}
    cuboid = {"position" : position, "size" : size}
    return cuboid

def min_cube_unused(cube):
    to_save = {}
    to_save = {"position" : cube["position"], "color" : cube["color"], "size" : cube["size"], "id" : cube["id"], "vertices" : None}
    return to_save

def face_equal(one, two):
    equal = False
    equal = ((one["axis"] == two["axis"]) and (one["sign"] == two["sign"]))
    return equal

def array_equal(a, b):
    yes = False
    if (len(a) != len(b)):
            yes = False
            return yes
    for i in range(int(len(a))):
            if (a[int(i)] != b[int(i)]):
                        yes = False
                        return yes
    yes = True
    return yes

def rotates_ortho_new(ang_one, axis_one, ang_two, axis_two):
    rotates = []
    rotates = [{"angle" : ang_one, "axis" : axis_one}, {"angle" : ang_two, "axis" : axis_two}]
    return rotates

def orient_new(right, front):
    orient = {}
    orient = {"right" : right, "front" : front}
    return orient

def cubes_get(cubes, position):
    cube = {}
    cube = None
    for element in cubes:
            if array_equal(element["position"], position):
                        cube = element
                        return cube
    return cube

def integer_array_string(integer_array):
    text = ""
    texts = []
    for integer in integer_array:
            texts.append(str(int(integer)))
    text = json.loads(texts)
    return text

def equal_axis(one, two, axis):
    same_axis = 0.0
    same_axis = None
    for i in range(3):
            if (i == axis):
                        continue
            if (one["position"][int(i)] == two["position"][int(i)]):
                        same_axis = i
    return same_axis

def neighbor_indices(indices, axis, sign):
    sum_indices = []
    sum_indices = [indices[0], indices[1], indices[2]]
    value = sign
    if (sign == 0.0):
            value = -1.0
    sum_indices[int(axis)] += value
    return sum_indices

def outer_direction(voxels, indices):
    axis = 0.0
    sign = 0.0
    if (((indices[0] < 0.0) or (indices[1] < 0.0)) or (indices[2] < 0.0)):
            outside = True
            return axis, sign
    if (((indices[2] >= len(voxels)) or (indices[1] >= len(voxels[0]))) or (indices[0] >= len(voxels[0][0]))):
            outside = True
            return axis, sign
    return axis, sign

def orientation_up(orientation):
    up = []
    up = cross_product(orientation["right"], orientation["front"])
    return up

def orientation_direction(orientation, axis, sign):
    direction = []
    right = orientation["right"]
    front = orientation["front"]
    up = orientation_up(orientation)
    if (axis == 0.0):
            if (sign == 1.0):
                        direction = right
            else:
                        direction = array_scaled(right, -1.0)
    elif (axis == 1.0):
            if (sign == 1.0):
                        direction = front
            else:
                        direction = array_scaled(front, -1.0)
    elif (axis == 2.0):
            if (sign == 1.0):
                        direction = up
            else:
                        direction = array_scaled(up, -1.0)
    return direction

def adjacent_face(face_axis, axis, sign):
    new_axis = 0.0
    new_sign = 0.0
    new_sign = sign
    new_axes = []
    for i in range(3):
            if (i == face_axis):
                        continue
            new_axes.append(i)
    new_axis = new_axes[int(axis)]
    return new_axis, new_sign

def adjacent_indices(indices, face_axis, axis, sign):
    adjacent = []
    new_axis = []
    for i in range(3):
            if (i == face_axis):
                        continue
            new_axis.append(i)
    adjacent = neighbor_indices(indices, new_axis[int(axis)], sign)
    return adjacent

def stack_indices(voxels, position, unit_size, point):
    indices = []
    lengths = [len(voxels[0][0]), len(voxels[0]), len(voxels)]
    for i in range(3):
            index = ((point[int(i)] - position[int(i)]) / unit_size)
            if (index >= lengths[int(i)]):
                        index = (lengths[int(i)] - 1.0)
            indices.append(index)
    return indices

def stack_position(stack, indices):
    position = []
    position = sum_arrays(stack["position"], array_scaled(indices, stack["unit_size"]))
    return position

def cubes_bounds(cubes):
    bounds = {}
    point = []
    size = []
    for i in range(3):
            min = cubes[0]["position"][int(i)]
            max = (min + cubes[0]["size"])
            for j in range(1, int(len(cubes))):
                        this_min = cubes[int(j)]["position"][int(i)]
                        this_max = (this_min + cubes[int(j)]["size"])
                        if (this_min < min):
                                        min = this_min
                        if (this_max > max):
                                        max = this_max
            point.append(min)
            size.append((max - point[int(i)]))
    bounds = cuboid_new(point, size)
    return bounds

def cuboids_bounds(cuboids):
    point = []
    size = []
    for i in range(3):
            min = cuboids[0]["position"][int(i)]
            max = (min + cuboids[0]["size"][int(i)])
            for j in range(1, int(len(cuboids))):
                        this_min = cuboids[int(j)]["position"][int(i)]
                        this_max = (this_min + cuboids[int(j)]["size"][int(i)])
                        if (this_min < min):
                                        min = this_min
                        if (this_max > max):
                                        max = this_max
            point.append(min)
            size.append((max - point[int(i)]))
    return point, size

def is_overlap_rectangles(one, two):
    yes = False
    one_position = one["position"]
    one_size = one["size"]
    two_position = two["position"]
    two_size = two["size"]
    two_max = [(two_position[0] + two_size[0]), (two_position[1] + two_size[1])]
    min = [one_position[0], one_position[1]]
    max = [(one_position[0] + one_size[0]), (one_position[1] + one_size[1])]
    for i in range(2):
            if (two_position[int(i)] < min[int(i)]):
                        min[int(i)] = two_position[int(i)]
            if (two_max[int(i)] > max[int(i)]):
                        max[int(i)] = two_max[int(i)]
    ranges = [(one_size[0] + two_size[0]), (one_size[1] + two_size[1])]
    for i in range(2):
            if ((max[int(i)] - min[int(i)]) >= ranges[int(i)]):
                        yes = False
                        return yes
    yes = True
    return yes

def is_overlap_cuboids(one_p, one_s, two_p, two_s):
    yes = False
    min = [one_p[0], one_p[1], one_p[2]]
    max = [(one_p[0] + one_s[0]), (one_p[1] + one_s[1]), (one_p[2] + one_s[2])]
    for i in range(3):
            if (two_p[int(i)] < min[int(i)]):
                        min[int(i)] = two_p[int(i)]
            two_max = (two_p[int(i)] + two_s[int(i)])
            if (two_max > max[int(i)]):
                        max[int(i)] = two_max
    ranges = [(one_s[0] + two_s[0]), (one_s[1] + two_s[1]), (one_s[2] + two_s[2])]
    for i in range(3):
            if ((max[int(i)] - min[int(i)]) >= ranges[int(i)]):
                        yes = False
                        return yes
    yes = True
    return yes

def axis_overlap_cuboids(one, one_size, two, two_size):
    axis = 0.0
    for i in range(3):
            one_rect = face_cuboid(one, one_size, i, 0.0)
            two_rect = face_cuboid(two, two_size, i, 0.0)
            if is_overlap_rectangles(one_rect, two_rect):
                        axis = i
                        return axis
    axis = None
    return axis
    return axis

def face_overlap(one, one_size, two, two_size):
    axis = 0.0
    sign = 0.0
    one_max = sum_arrays(one, one_size)
    two_max = sum_arrays(two, two_size)
    for i in range(3):
            if (one[int(i)] == two_max[int(i)]):
                        one_rect = face_cuboid(one, one_size, i, 0.0)
                        two_rect = face_cuboid(two, two_size, i, 1.0)
                        if is_overlap_rectangles(one_rect, two_rect):
                                        axis = i
                                        sign = 0.0
                                        return axis, sign
    for i in range(3):
            if (one_max[int(i)] == two[int(i)]):
                        one_rect = face_cuboid(one, one_size, i, 1.0)
                        two_rect = face_cuboid(two, two_size, i, 0.0)
                        if is_overlap_rectangles(one_rect, two_rect):
                                        axis = i
                                        sign = 1.0
                                        return axis, sign
    axis = None
    sign = None
    return axis, sign
    return axis, sign

def nullify_input(normal, input):
    output = []
    n0 = normal[0]
    n1 = normal[1]
    n2 = normal[2]
    i0 = input[0]
    i1 = input[1]
    i2 = input[2]
    output = [input[0], input[1], input[2]]
    if (((i0 > 0.0) and (n0 > 0.0)) or ((i0 < 0.0) and (n0 < 0.0))):
            output[0] = 0.0
    elif (((i1 > 0.0) and (n1 > 0.0)) or ((i1 < 0.0) and (n1 < 0.0))):
            output[1] = 0.0
    elif (((i2 > 0.0) and (n2 > 0.0)) or ((i2 < 0.0) and (n2 < 0.0))):
            output[2] = 0.0
    return output

def bounds_geometry(geometry):
    bounds = {}
    vertex = geometry[0]
    min = [vertex[0], vertex[1], vertex[2]]
    max = [vertex[0], vertex[1], vertex[2]]
    for i in range(1, int(len(geometry))):
            vertex = geometry[int(i)]
            for j in range(3):
                        num = vertex[int(j)]
                        if (num < min[int(j)]):
                                        min[int(j)] = num
                        elif (num > max[int(j)]):
                                        max[int(j)] = num
    size = subtract_arrays(max, min)
    bounds = cuboid_new(min, size)
    return bounds

def matrix_translate(position):
    new_matrix = []
    new_matrix = [[1.0, 0.0, 0.0, position[0]], [0.0, 1.0, 0.0, position[1]], [0.0, 0.0, 1.0, position[2]], [0.0, 0.0, 0.0, 1.0]]
    return new_matrix

def translate(position, direction, scale):
    new_position = []
    new_position = sum_arrays(position, array_scaled(direction, scale))
    return new_position

def rotate(vector, angle, axis):
    new_vector = []
    matrix = rotation_matrix(angle, axis[0], axis[1], axis[2])
    new_vector = product_matrix_array(matrix, vector)
    return new_vector

def vector_axis_sign_scaled(axis, sign, scale):
    vector = []
    vector = [0.0, 0.0, 0.0]
    if (sign == 0.0):
            scale *= -1.0
    vector[int(axis)] = scale
    return vector

def vector_axis_sign(axis, sign):
    normal = []
    value = -1.0
    if (sign == 1.0):
            value = 1.0
    normal = [0.0, 0.0, 0.0]
    normal[int(axis)] = value
    return normal

def vectors_component(vector):
    vectors = []
    if (vector[0] != 0.0):
            vectors.append([vector[0], 0.0, 0.0])
    if (vector[1] != 0.0):
            vectors.append([0.0, vector[1], 0.0])
    if (vector[2] != 0.0):
            vectors.append([0.0, 0.0, vector[2]])
    return vectors

def vectors_component_unit(vector):
    vectors = []
    if (vector[0] > 0.0):
            vectors.append([1.0, 0.0, 0.0])
    elif (vector[0] < 0.0):
            vectors.append([-1.0, 0.0, 0.0])
    if (vector[1] > 0.0):
            vectors.append([0.0, 1.0, 0.0])
    elif (vector[1] < 0.0):
            vectors.append([0.0, -1.0, 0.0])
    if (vector[2] > 0.0):
            vectors.append([0.0, 0.0, 1.0])
    elif (vector[2] < 0.0):
            vectors.append([0.0, 0.0, -1.0])
    return vectors

def axis_sign_vector(vector):
    axis = 0.0
    sign = 0.0
    for i in range(3):
            axis = i
            if (vector[int(i)] < 0.0):
                        sign = 0.0
                        return axis, sign
            elif (vector[int(i)] > 0.0):
                        sign = 1.0
                        return axis, sign
    return axis, sign

def time_point_plane(point, plane_point, normal):
    time = 0.0
    i = subtract_arrays(plane_point, point)
    ldotn = (((normal[0] * normal[0]) + (normal[1] * normal[1])) + (normal[2] * normal[2]))
    time = ((((i[0] * normal[0]) + (i[1] * normal[1])) + (i[2] * normal[2])) / ldotn)
    return time

def distance_directional(vector, one_p, one_s, two_p, two_s):
    time = 0.0
    begin = point_farthest(one_p, one_s, vector)
    end = point_farthest(two_p, two_s, array_scaled(vector, -1.0))
    i = subtract_arrays(end, begin)
    ldotn = (((vector[0] * vector[0]) + (vector[1] * vector[1])) + (vector[2] * vector[2]))
    time = ((((i[0] * vector[0]) + (i[1] * vector[1])) + (i[2] * vector[2])) / ldotn)
    return time

def point_farthest(position, size, vector):
    max_point = []
    points = points_cuboid(position, size)
    line_point = points[0]
    max_time = 0.0
    max_point = line_point
    ldotn = (((vector[0] * vector[0]) + (vector[1] * vector[1])) + (vector[2] * vector[2]))
    for i in range(1, 8):
            plane_point = points[int(i)]
            t = subtract_arrays(plane_point, line_point)
            time = ((((t[0] * vector[0]) + (t[1] * vector[1])) + (t[2] * vector[2])) / ldotn)
            if (time > max_time):
                        max_time = time
                        max_point = plane_point
    return max_point

def corner_point(position, size, corner):
    point = []
    point = [position[0], position[1], position[2]]
    for i in range(3):
            point[int(i)] += (size[int(i)] * corner[int(i)])
    return point

def points_cuboid(p, s):
    points = []
    points = [[p[0], p[1], p[2]], [(p[0] + s[0]), p[1], p[2]], [(p[0] + s[0]), (p[1] + s[1]), p[2]], [p[0], (p[1] + s[1]), p[2]], [p[0], p[1], (p[2] + s[2])], [(p[0] + s[0]), p[1], (p[2] + s[2])], [(p[0] + s[0]), (p[1] + s[1]), (p[2] + s[2])], [p[0], (p[1] + s[1]), (p[2] + s[2])]]
    return points

def get_corners(axis, sign):
    corners = []
    if (axis == 0.0):
            corners = [[sign, 0.0, 0.0], [sign, 1.0, 0.0], [sign, 1.0, 1.0], [sign, 0.0, 1.0]]
    elif (axis == 1.0):
            corners = [[0.0, sign, 0.0], [0.0, sign, 1.0], [1.0, sign, 1.0], [1.0, sign, 0.0]]
    else:
            corners = [[0.0, 0.0, sign], [1.0, 0.0, sign], [1.0, 1.0, sign], [0.0, 1.0, sign]]
    return corners

def triangles_cuboid_face(position, size, axis, sign, color):
    triangles = []
    corners = get_corners(axis, sign)
    points = []
    normal = vector_axis_sign(axis, sign)
    for i in range(4):
            corner = corners[int(i)]
            point = corner_point(position, size, corner)
            points.append(point)
    ins = [3.0, 2.0, 1.0, 0.0]
    if (sign == 1.0):
            ins = [0.0, 1.0, 2.0, 3.0]
    indices_pair = [[0.0, 1.0, 2.0], [2.0, 3.0, 0.0]]
    triangles = []
    for indices in indices_pair:
            for i in indices:
                        vertex = []
                        vertex.extend(points[int(ins[int(i)])])
                        vertex.extend(normal)
                        vertex.extend(color)
                        triangles.append(vertex)
    return triangles

def matrix_placement(position, rotates):
    new_matrix = []
    new_matrix = matrix_translate(position)
    for rotate in rotates:
            matrix = matrix_rotate_ortho(rotate["angle"], rotate["axis"])
            new_matrix = product_matrices(new_matrix, matrix)
    return new_matrix

def matrix_rotate_ortho(angle, axis):
    matrix = []
    cos_ang = 0.0
    sin_ang = 0.0
    if (angle == 0.0):
            cos_ang = 1.0
            sin_ang = 0.0
    elif (angle == 90.0):
            cos_ang = 0.0
            sin_ang = 1.0
    elif (angle == 180.0):
            cos_ang = -1.0
            sin_ang = 0.0
    elif (angle == 270.0):
            cos_ang = 0.0
            sin_ang = -1.0
    x = 1.0
    y = 0.0
    z = 0.0
    if (axis == 1.0):
            x = 0.0
            y = 1.0
            z = 0.0
    elif (axis == 2.0):
            x = 0.0
            y = 0.0
            z = 1.0
    matrix = [[(cos_ang + ((x * x) * (1.0 - cos_ang))), (((x * y) * (1.0 - cos_ang)) - (z * sin_ang)), (((x * z) * (1.0 - cos_ang)) + (y * sin_ang)), 0.0], [(((y * x) * (1.0 - cos_ang)) + (z * sin_ang)), (cos_ang + ((y * y) * (1.0 - cos_ang))), (((y * z) * (1.0 - cos_ang)) - (x * sin_ang)), 0.0], [(((z * x) * (1.0 - cos_ang)) - (y * sin_ang)), (((z * y) * (1.0 - cos_ang)) + (x * sin_ang)), (cos_ang + ((z * z) * (1.0 - cos_ang))), 0.0], [0.0, 0.0, 0.0, 1.0]]
    return matrix

def rotation_matrix(ang, x, y, z):
    matrix = []
    matrix = [[(math.cos(ang) + ((x * x) * (1.0 - math.cos(ang)))), (((x * y) * (1.0 - math.cos(ang))) - (z * math.sin(ang))), (((x * z) * (1.0 - math.cos(ang))) + (y * math.sin(ang)))], [(((y * x) * (1.0 - math.cos(ang))) + (z * math.sin(ang))), (math.cos(ang) + ((y * y) * (1.0 - math.cos(ang)))), (((y * z) * (1.0 - math.cos(ang))) - (x * math.sin(ang)))], [(((z * x) * (1.0 - math.cos(ang))) - (y * math.sin(ang))), (((z * y) * (1.0 - math.cos(ang))) + (x * math.sin(ang))), (math.cos(ang) + ((z * z) * (1.0 - math.cos(ang))))]]
    return matrix

def point_transformed(matrix, p):
    transformed = []
    transformed = product_matrix_array(matrix, [p[0], p[1], p[2], 1.0])
    transformed.pop()
    return transformed

def product_matrix_array(matrix, vector):
    out_vector = []
    for row in matrix:
            sum = 0.0
            for i in range(int(len(vector))):
                        sum += (row[int(i)] * vector[int(i)])
            out_vector.append(sum)
    return out_vector

def product_matrices(one, two):
    product = []
    for one_row in one:
            row = []
            for j in range(4):
                        sum = 0.0
                        for k in range(4):
                                        sum += (one_row[int(k)] * two[int(k)][int(j)])
                        row.append(sum)
            product.append(row)
    return product

def sum_arrays(a, b):
    sum = []
    for i in range(int(len(a))):
            sum.append((a[int(i)] + b[int(i)]))
    return sum

def subtract_arrays(a, b):
    sum = []
    for i in range(int(len(a))):
            sum.append((a[int(i)] - b[int(i)]))
    return sum

def array_scaled(a, b):
    product = []
    for i in range(int(len(a))):
            product.append((a[int(i)] * b))
    return product

def matrix_identity():
    identity = []
    identity = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
    return identity

def ortho_make(left, right, bottom, top, zNear, zFar):
    matrix = []
    tx = ((-1.0 * (right + left)) / (right - left))
    ty = ((-1.0 * (top + bottom)) / (top - bottom))
    tz = ((-1.0 * (zFar + zNear)) / (zFar - zNear))
    matrix = [[(2.0 / (right - left)), 0.0, 0.0, tx], [0.0, (2.0 / (top - bottom)), 0.0, ty], [0.0, 0.0, (-2.0 / (zFar - zNear)), tz], [0.0, 0.0, 0.0, 1.0]]
    return matrix

def perspective_make(fovy, aspect, z_near, z_far):
    perspective = []
    f = (1.0 / math.tan((fovy / 2.0)))
    perspective = [[(f / aspect), 0.0, 0.0, 0.0], [0.0, f, 0.0, 0.0], [0.0, 0.0, ((z_far + z_near) / (z_near - z_far)), (((2.0 * z_far) * z_near) / (z_near - z_far))], [0.0, 0.0, -1.0, 0.0]]
    return perspective

def cross_product(x, y):
    cross = []
    cross = [((x[1] * y[2]) - (x[2] * y[1])), ((x[2] * y[0]) - (x[0] * y[2])), ((x[0] * y[1]) - (x[1] * y[0]))]
    return cross

def vector_unit(vector):
    unit_vector = []
    magnitude = magnitude_vector(vector)
    for item in vector:
            unit_vector.append((item / magnitude))
    return unit_vector

def magnitude_vector(vector):
    magnitude = 0.0
    sum_square = 0.0
    for i in range(int(len(vector))):
            sum_square += (vector[int(i)] * vector[int(i)])
    magnitude = math.sqrt(sum_square)
    return magnitude

def look_at_make(eye, center, up):
    look_at = []
    F = [(center[0] - eye[0]), (center[1] - eye[1]), (center[2] - eye[2])]
    f_mag = magnitude_vector(F)
    f = [(F[0] / f_mag), (F[1] / f_mag), (F[2] / f_mag)]
    up_mag = magnitude_vector(up)
    up_unit = [(up[0] / up_mag), (up[1] / up_mag), (up[2] / up_mag)]
    s = cross_product(f, up_unit)
    u = cross_product(s, f)
    t0 = ((((-1.0 * eye[0]) * s[0]) + ((-1.0 * eye[1]) * s[1])) + ((-1.0 * eye[2]) * s[2]))
    t1 = ((((-1.0 * eye[0]) * u[0]) + ((-1.0 * eye[1]) * u[1])) + ((-1.0 * eye[2]) * u[2]))
    t2 = (((eye[0] * f[0]) + (eye[1] * f[1])) + (eye[2] * f[2]))
    look_at = [[s[0], s[1], s[2], t0], [u[0], u[1], u[2], t1], [(-1.0 * f[0]), (-1.0 * f[1]), (-1.0 * f[2]), t2], [0.0, 0.0, 0.0, 1.0]]
    return look_at

def direction_from_camera(orient, FOVY, resolution, position):
    direction = []
    width = ((math.tan((FOVY / 2.0)) * resolution[0]) / resolution[1])
    height = math.tan((FOVY / 2.0))
    middleX = (resolution[0] / 2.0)
    middleY = (resolution[1] / 2.0)
    width_point = (((position[0] - middleX) / middleX) * width)
    height_point = (((position[1] - middleY) / middleY) * height)
    direction = orient["front"]
    direction = sum_arrays(direction, array_scaled(orientation_up(orient), height_point))
    direction = sum_arrays(direction, array_scaled(orient["right"], width_point))
    direction = vector_unit(direction)
    return direction

def is_point_in_rectangle(point, position, size):
    yes = False
    for i in range(2):
            if ((point[int(i)] < position[int(i)]) or (point[int(i)] > (position[int(i)] + size[int(i)]))):
                        yes = False
                        return yes
    yes = True
    return yes

def cuboid_transformed(matrix, position, size):
    new_position = []
    new_size = []
    two = sum_arrays(position, size)
    new_one = point_transformed(matrix, position)
    new_two = point_transformed(matrix, two)
    new_position = []
    new_far = []
    for i in range(3):
            if (new_one[int(i)] < new_two[int(i)]):
                        new_position.append(new_one[int(i)])
                        new_far.append(new_two[int(i)])
            else:
                        new_position.append(new_two[int(i)])
                        new_far.append(new_one[int(i)])
    new_size = subtract_arrays(new_far, new_position)
    return new_position, new_size

def adjacent_cubes(position, side, axis):
    faces = []
    x = position[0]
    y = position[1]
    z = position[2]
    values = [(-1.0 * side), side]
    for i in range(3):
            if (i == axis):
                        continue
            sign_faces = []
            for value in values:
                        position = [x, y, z]
                        position[int(i)] += value
                        sign_faces.append({"position" : position, "size" : side})
            faces.append(sign_faces)
    return faces

def adjacent_squares(position, side, face):
    faces = []
    x = position[0]
    y = position[1]
    z = position[2]
    axis = face["axis"]
    values = [(-1.0 * side), side]
    for i in range(3):
            if (i == axis):
                        continue
            sign_faces = []
            for value in values:
                        position = [x, y, z]
                        position[int(i)] += value
                        if (face["sign"] == 1.0):
                                        position[int(axis)] += side
                        sign_faces.append({"position" : position, "size" : side, "axis" : axis})
            faces.append(sign_faces)
    return faces

def is_close_to_zero(value):
    yes = False
    if ((value > -1e-05) and (value < 1e-05)):
            yes = True
    else:
            yes = False
    return yes

def is_close(a, b, buffer):
    yes = False
    c = abs((a - b))
    if (c < buffer):
            yes = True
    return yes

def is_close_vector_3(a, b, buffer):
    yes = False
    yes = True
    for i in range(3):
            if (is_close(a[int(i)], b[int(i)], buffer) == False):
                        yes = False
    return yes

def ray_to_rectangle_time(o, d, p, n):
    t = 0.0
    dot_product = (((d[0] * n[0]) + (d[1] * n[1])) + (d[2] * n[2]))
    if is_close_to_zero(dot_product):
            t = None
            return t
    D = (-1.0 * (((n[0] * p[0]) + (n[1] * p[1])) + (n[2] * p[2])))
    numerator = (-1.0 * ((((n[0] * o[0]) + (n[1] * o[1])) + (n[2] * o[2])) + D))
    t = (numerator / dot_product)
    return t

def intersect_ray_rectangle(origin, direction, position, size, axis):
    intersect_point = []
    normal = vector_axis_sign(axis, 1.0)
    t = ray_to_rectangle_time(origin, direction, position, normal)
    if (t == None):
            intersect_point = None
            return intersect_point
    on_plane = []
    plane_position = []
    intersect_point = sum_arrays(origin, array_scaled(direction, t))
    for i in range(3):
            if (i != axis):
                        on_plane.append(intersect_point[int(i)])
                        plane_position.append(position[int(i)])
    if (is_point_in_rectangle(on_plane, plane_position, size) == False):
            intersect_point = None
    return intersect_point

def axis_signs_visible(direction):
    faces = []
    x = direction[0]
    y = direction[1]
    z = direction[2]
    faces = []
    if (x > 0.0):
            faces.append(axis_sign_new(0.0, 0.0))
    elif (x < 0.0):
            faces.append(axis_sign_new(0.0, 1.0))
    if (y > 0.0):
            faces.append(axis_sign_new(1.0, 0.0))
    elif (y < 0.0):
            faces.append(axis_sign_new(1.0, 1.0))
    if (z > 0.0):
            faces.append(axis_sign_new(2.0, 0.0))
    elif (z < 0.0):
            faces.append(axis_sign_new(2.0, 1.0))
    return faces

def cube_square(position, size, axis, sign):
    square = {}
    square_position = [position[0], position[1], position[2]]
    if (sign != 0.0):
            vector = vector_axis_sign_scaled(axis, sign, size)
            square_position = sum_arrays(position, vector)
    square = new_square(square_position, size, axis)
    return square

def face_cuboid(position, size, axis, sign):
    face = {}
    face_position = [position[0], position[1], position[2]]
    if (sign != 0.0):
            vector = vector_axis_sign_scaled(axis, sign, size[int(axis)])
            face_position = sum_arrays(position, vector)
    new_position = []
    new_size = []
    for i in range(3):
            if (i != axis):
                        new_position.append(face_position[int(i)])
                        new_size.append(size[int(i)])
    face = rectangle_2d_new(new_position, new_size)
    return face

def intersect_ray_cuboid_face(origin, direction, position, size, axis, sign):
    intersect_point = []
    square_position = [position[0], position[1], position[2]]
    if (sign != 0.0):
            vector = vector_axis_sign_scaled(axis, sign, size[int(axis)])
            square_position = sum_arrays(position, vector)
    rectangle_size = []
    for i in range(3):
            if (i == axis):
                        continue
            rectangle_size.append(size[int(i)])
    intersect_point = intersect_ray_rectangle(origin, direction, square_position, rectangle_size, axis)
    return intersect_point

def next_face(position, size, point):
    face = []
    min_x = position[0]
    max_x = (position[0] + size)
    min_y = position[1]
    max_y = (position[1] + size)
    min_z = position[2]
    max_z = (position[2] + size)
    if (point[1] > max_y):
            face = [1.0, 1.0]
    elif (point[1] < min_y):
            face = [1.0, 0.0]
    elif (point[0] > max_x):
            face = [0.0, 1.0]
    elif (point[0] < min_x):
            face = [0.0, 0.0]
    elif (point[2] > max_z):
            face = [2.0, 1.0]
    elif (point[2] < min_z):
            face = [2.0, 0.0]
    return face

def vertices_cube(position, size, byte_color, tick):
    triangles = []
    triangles = vertices_cuboid(position, [size, size, size], byte_color, tick)
    return triangles

def vertices_cuboid(position, size, byte_color, tick):
    triangles = []
    offset = [(position[0] + tick), (position[1] + tick), (position[2] + tick)]
    new_size = [(size[0] - (2.0 * tick)), (size[1] - (2.0 * tick)), (size[2] - (2.0 * tick))]
    color = []
    for digit in byte_color:
            color.append((digit / 255.0))
    for axis in range(3):
            for sign in range(2):
                        triangles.extend(triangles_cuboid_face(offset, new_size, axis, sign, color))
    return triangles

