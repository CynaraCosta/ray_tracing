import numpy as np
from geo_objects import Plane, Sphere, Triangle

def normalize(vector):
    return vector / np.linalg.norm(vector)

def reflect(l, n):
    result = 2 * n * (np.dot(l, n)) - l 
    return result

def refract(obj, v, n):
    #Cálculo do coseno do ângulo de incidência
    normal = n
    cos = np.dot(n,v)
    #Índice de refração relativo
    irr = obj.Nr

    #Se o ângulo for obtuso
    if cos < 0:
        normal *= -1
        irr = 1/irr # Invertido os meios
        cos *= -1

    delta = 1 - ((1/(irr**2)) * (1 - cos**2))
    # Se for uma reflexão total:
    if delta < 0:
        raise Exception ('Total Internal Reflection Exception')
    # Cálculo do raio refratado
    return (-1/irr * v) - (np.sqrt(delta) - (1/irr * cos))*normal 

def nearest(objs, point_O, vector_d):
    closest = None
    t_min = np.inf # numero mt grande para identificar que n ha interseccoes

    for obj in objs:
        t = obj.intersection(point_O, vector_d)

        if t and t < t_min:
            closest = obj
            t_min = t
    
    return t_min, closest

def shade(obj, objs, P, vector_d, normal_obj_p, lights, ca):
    final_color_point = obj.Ka * ca * obj.color
    for cj, Lj in lights:
        lj = normalize(Lj - P)
        rj = reflect(lj, normal_obj_p)

        new_point = P + 10E-5*lj

        t, shadow = nearest(objs, new_point, lj)

        if  not shadow or (np.dot(lj, (Lj - new_point)) < t): # not shadow = n intercepta c nenhum objeto portanto n ta na sombra
            if np.dot(normal_obj_p,lj) > 0:
                final_color_point = final_color_point + ((obj.Kd*obj.color) * np.dot(normal_obj_p,lj) * cj)

            if np.dot(vector_d, rj) > 0:
                final_color_point = final_color_point + (obj.Ks * (np.dot(vector_d, rj))**obj.n * cj )

    return final_color_point

def filter_two(objs, point_O, vector_d, bg_color, ca, lights,ttl,e=10E-5):
    color_to_return = bg_color
    t, closest = nearest(objs, point_O, vector_d)
    if closest: 
        point = point_O + (t*vector_d)
        v = -vector_d
        n = closest.normal(point)
        color_to_return = shade(closest, objs, point, v, n, lights, ca)
        if ttl != 0:
            Rr = reflect(v, n)
            Pr = point + Rr*e
            try:
                if closest.Kt > 0:
                    Rt = refract(closest, v, n)
                    Pt = point + e*Rt
                    color_to_return = color_to_return + closest.Kt * filter_two(objs,Pt,Rt,color_to_return,ca,lights,ttl-1)
                if closest.Kr > 0:
                    color_to_return = color_to_return + closest.Kr * filter_two(objs,Pr,Rr,color_to_return,ca,lights,ttl-1)
            except:
                color_to_return = color_to_return + filter_two(objs,Pr,Rr,color_to_return,ca,lights,ttl-1)


    return color_to_return

def render(v_res, h_res, square_side, dist, eye, look_at, up, background_color, objs, lights, ca, depth):
    w = normalize(eye - look_at)
    u = normalize(np.cross(up, w))
    v = np.cross(w, u)

    center = eye - (w * dist)

    Q = np.zeros((v_res, h_res, 3))
    # array_pixel = np.zeros((v_res, h_res, 3))
    img = np.full((v_res, h_res, 3), background_color)

    Q[0,0] = center + (1/2 * square_side * (v_res - 1) * v) - (1/2 * square_side * (h_res - 1) * u)

    for i in range(v_res):
        for j in range(h_res):
            Q[i,j] = Q[0,0] + (square_side * (j * u)) - (square_side * (i * v))
            line = normalize(Q[i,j] - eye)
            
            placeH = filter_two(objs,eye,line,background_color,ca,lights,depth)
            placeH = placeH/max(*placeH, 1)

            img[i][j] = placeH       

    return img  
