from asyncio.windows_events import NULL
import numpy as np
from geo_objects import Plane, Sphere, Triangle

def normalize(vector):
    return vector / np.linalg.norm(vector)

def reflect(l, n):
    result = 2 * n * (np.dot(l, n)) - l 

def filter_one(objs, point_O, vector_d):
    interceptions = []

    for obj in objs:
        t = obj.intersection(point_O, vector_d)

        if t:
            # if there is a interception, is going to return the locate = t and which obj it is
            interceptions.append((t, obj))
    return interceptions

def shade(obj, objs, P, vector_d, normal_obj_p, lights, ca):
    final_color_point = obj.Ka * ca * obj.color
    for cj, Lj in lights:
        lj = normalize(Lj - P)
        rj = reflect(lj, normal_obj_p)

        new_point = P + 10E-5*lj

        S = filter_one(objs, new_point, lj)
        S.sort()

        t = 0
        if len(S) != 0:
            t, obj = S[0]

        if len(S) == 0 or (np.dot(lj, (Lj - new_point)) < t):
            if np.dot(normal_obj_p,lj) > 0:
                final_color_point = final_color_point + ((obj.Kd*obj.color) * np.dot(normal_obj_p,lj) * cj)

            if np.dot(vector_d, rj) > 0:
                final_color_point = final_color_point + (obj.Ks * (np.dot(vector_d, rj))**obj.n * cj )

    return final_color_point

def filter_two(objs, point_O, vector_d, bg_color, ca, lights): # cast
    color_to_return = bg_color
    interceptions = filter_one(objs, point_O, vector_d)

    # sorting to see which is the closest object
    interceptions.sort()

    if len(interceptions) != 0:
        # if there is objects at the screen we are going to get this object and see his color
        t, obj = interceptions[0]
        point = point_O + (t*vector_d)
        color_to_return = shade(obj, objs, point, -vector_d, obj.normal(point), lights, ca)

    # we are going to return this color, because if there is no obj is going to be the bg_color, otherwise the obj_color
    return color_to_return

def render(v_res, h_res, square_side, dist, eye, look_at, up, background_color, objs, lights, ca):
    w = normalize(eye - look_at)
    u = normalize(np.cross(up, w))
    v = np.cross(w, u)

    center = eye - (w * dist)

    Q = np.zeros((v_res, h_res, 3))
    array_pixel = np.zeros((v_res, h_res, 3))

    Q[0,0] = center + (1/2 * square_side * (v_res - 1) * v) - (1/2 * square_side * (h_res - 1) * u)

    for i in range(v_res):
        for j in range(h_res):
            Q[i,j] = Q[0,0] + (square_side * (j * u)) - (square_side * (i * v))
            line = normalize(Q[i,j] - eye)
            
            array_pixel[i, j] = filter_two(objs, eye, line, background_color, ca, lights)
            

    return array_pixel / 255
