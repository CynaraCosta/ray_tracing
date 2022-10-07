import numpy as np
from geo_objects import Plane, Sphere, Triangle

def normalize(vector):
    return vector / np.linalg.norm(vector)


def filter_one(objs, point_O, vector_d):
    interceptions = []

    for obj in objs:
        t = obj.intersection(point_O, vector_d)

        if t:
            # if there is a interception, is going to return the locate = t and which obj it is
            interceptions.append((t, obj))
    return interceptions

def filter_two(objs, point_O, vector_d, bg_color):
    color_to_return = bg_color
    interceptions = filter_one(objs, point_O, vector_d)

    # sorting to see which is the closest object
    interceptions.sort()

    if len(interceptions) != 0:
        # if there is objects at the screen we are going to get this object and see his color
        closest = interceptions[0][1]
        color_to_return = closest.color

    # we are going to return this color, because if there is no obj is going to be the bg_color, otherwise the obj_color
    return color_to_return

def render(v_res, h_res, square_side, dist, eye, look_at, up, bg_color, objs):
    w = normalize(eye - look_at)
    u = normalize(np.cross(up, w))
    v = np.cross(w, u)

    center = eye - (w * dist)

    Qzero = center + (1/2 * square_side * (v_res - 1) * v) - (1/2 * square_side * (h_res - 1) * u)

    j, i = 0, 0
    Qarb = Qzero + (square_side * (j * u)) - (square_side * (i * v))
