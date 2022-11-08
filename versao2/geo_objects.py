import numpy as np

def projecao(u, v):
    # projecao(u, v) = ((np.dot(v, u) / abs(np.dot(v,v))) * v )
    vector = ((np.dot(v, u)/ abs(np.dot(v,v))) * v )
    return vector

class Object:
    # class to store the colors from a object
    # np.array gets tuple to turn the values into a array
    def set_color(self, rgb):
        self.color = rgb

    def set_lights(self, Ka, Kd, Ks, n):
        self.Ka = Ka
        self.Kd = Kd
        self.Ks = Ks
        self.n = n

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

    def normal(self, point):
        result = (self.normal_vector) / np.linalg.norm(self.normal_vector)
        return result


    def __str__(self):
        return "Plane"

class Sphere(Object):
    def __init__(self, center, radius):
        self.radius = radius
        self.center = center

    def intersection(self, point_O, vector_d):
        vector_l = self.center - point_O
        t_min = np.dot(vector_l, vector_d)
        dist_center_to_point_sqrt = np.dot(vector_l, vector_l) - (t_min**2)

        if dist_center_to_point_sqrt > (self.radius ** 2):
            return None
        
        else:
            delta = (self.radius**2 - dist_center_to_point_sqrt)**(1/2)
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

    def normal(self, point):
        result = (point - self.center) / np.linalg.norm(point - self.center)
        return result

    def __str__(self):
        return "Sphere"

class Triangle(Object):
    def __init__(self, point_a, point_b, point_c):
        self.point_a = np.array(point_a)
        point_b = np.array(point_b)
        point_c = np.array(point_c)

        vector_u = point_b - point_a
        vector_v = point_c - point_a

        self.plane = Plane(self.point_a, np.cross(vector_u, vector_v))

        hb = vector_u - projecao(vector_u, vector_v)
        hc = vector_v - projecao(vector_v, vector_u)

        self.hb = np.dot(((np.dot(hb, hb)) ** -1), hb)
        self.hc =  np.dot(((np.dot(hc, hc)) ** -1), hc)

    def intersection(self, point_O, vector_d):
        t = self.plane.intersection(point_O, vector_d)

        if t != None:
            point_p = point_O + (vector_d * t)
            vector_v = point_p - self.point_a

            beta = np.dot(vector_v, self.hb)
            gama = np.dot(vector_v, self.hc)
            alfa = 1 - (beta + gama)

            if 0 <= alfa <= 1 and 0 <= beta <= 1 and  0 <= gama <= 1:
                # there is intersection
                return t
        
        # there is no intersection
        else: 
            return None

    def normal(self, point):
        result = (self.plane.normal_vector) / np.linalg.norm(self.plane.normal_vector)
        return result

    def __str__(self):
        return "Triangle"