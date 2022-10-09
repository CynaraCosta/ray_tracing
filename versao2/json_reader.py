import json
from tokenize import Special
import numpy as np
from geo_objects import Plane, Sphere, Triangle

def getting_points(lista):
    point_a = []
    point_b = []
    point_c = []
    count = 0

    for lista in data:
        if count == 0:
            point_a = lista
            count += 1

        elif count == 1:
            point_b = lista
            count += 1

        else:
            point_c = lista

    return point_a, point_b, point_c

def get_path_and_infos(name):
    path = f"inputs/{name}.json"
    with open(path) as file:
        objects = []
        data = json.load(file)
        v_res = data["v_res"]
        h_res = data["h_res"]
        square_side = data["square_side"]
        dist = data["dist"]
        eye = np.array(data["eye"])
        look_at = np.array(data["look_at"])
        up = np.array(data["up"])
        background_color = np.array(data["background_color"])

        # getting the objects
        for object in data["objects"]:
            if "plane" in object:
                plane = Plane(np.array(object["plane"]["sample"]), np.array(object["plane"]["normal"]))
                plane.set_color(np.array(object["color"]))
                # get ilumination info

            if "sphere" in object:
                sphere = Sphere(np.array(object["sphere"]["center"]), object["sphere"]["radius"])
                sphere.set_color(np.array(object["color"]))
                # get ilumination info

            if "triangle" in object:
                point_a, point_b, point_c = getting_points(object["triangle"])
                triangle = Triangle(point_a, point_b, point_c)
                triangle.set_color(np.array(object["color"]))
                # get ilumination info

        ambient_light = np.array(data["ambient_light"])
        light_intensity = []
        light_position = []

        for light in data["lights"]:
            light_intensity = np.array(light["intensity"])
            light_position = np.array(light["position"])
        
        # do something with the info
