from re import T
import numpy as np

def projecao(u, v):
    # projecao(u, v) = ((np.dot(v, u) / abs(np.dot(v,v))) * v )
    vector = ((np.dot(v, u)/ abs(np.dot(v,v))) * v )
    return vector

class Object:
    # class to store the colors from a object
    # np.array gets tuple to turn the values into a array
    def set_color(self, rgb):
        self.color = np.array(rgb)

class Plane(Object):
    def __init__(self, point, normal_vector):
        self.point = np.array(point)
        self.normal_vector = np.array(normal_vector)

    def intersection(self, point_O, vector_d):
        constant_e = 1e-6
        # np.dot to do multiplication between vectors
        # want to check if they are parallels
        vector_v = np.dot(self.normal_vector, vector_d)

        if abs(vector_v) >= constant_e:
            height = np.dot((self.point - point_O), self.normal_vector)
            distance = height / vector_v
            if distance > constant_e:
                return distance
    
        # not intersection
        return None

    def __str__(self):
        return "Plane"

class Sphere(Object):
    def __init__(self, radius, center):
        self.radius = radius
        self.center = center

    def intersection(self, point_O, vector_d):
        vector_l = self.center - point_O
        t_min = np.dot(vector_l, vector_d)
        dist_center_to_point_sqrt = np.dot(vector_l, vector_l) - (t_min**2)

        if dist_center_to_point_sqrt > (self.radius ** 2):
            return None
        
        else:
            delta = ((self.radius **  2) - (dist_center_to_point_sqrt ** 2 ) ** 1/2)
            tl, tr = (t_min - delta, t_min + delta)

            if tl > tr:
                tl, tr = tr, tl

            elif tl < 0:
                if tr < 0:
                   return None 
                else:
                    return tr
            
            else: 
                return tl

    def __str__(self):
        return "Sphere"

class Triangle(Object):
    def __init__(self, point_a, point_b, point_c):
        self.point_a = point_a
        self.point_b = point_b
        self.point_c = point_c

        self.vector_u = point_b - point_a
        self.vector_v = point_c - point_a

        hb = self.vector_u - projecao(self.vector_u, self.vector_v)
        hc = self.vector_v - projecao(self.vector_v, self.vector_u)

        self.hb = np.dot(((np.dot(hb, hb)) ** -1), hb)
        self.hc =  np.dot(((np.dot(hc, hc)) ** -1), hc)

    def intersection(self, point_O, vector_d):
        normal_triangle = np.cross(self.point_a, self.point_b)
        triangle_plane = Plane(self.point_a, normal_triangle, point_O, vector_d)

        t = triangle_plane.intersection(point_O, vector_d)

        point_p = point_O + (vector_d * t)
        vector_v = point_p - self.point_a

        beta = np.dot(vector_v, self.hb)
        gama = np.dot(vector_v, self.hc)
        alfa = 1 - (beta + gama)

        if 0 <= alfa <= 1 and 0 <= beta <= 1 and  0 <= gama <= 1:
            # there is intersection
            return t
        
        # there is no intersection
        return None

    def __str__(self):
        return "Triangle"