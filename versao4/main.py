import matplotlib.pyplot as plt
import numpy as np
from geo_objects import Plane, Sphere
from render import render
from json_reader import get_path_and_infos

def change_type_input(Type):
    return map(Type, input().split())

def change_type_string(Type, string):
    return map(Type, string.split())

if __name__ == "__main__":
    # call the render here
    # image = render(v_res, h_res, square_side, dist, eye, look_at, up, bg_color, objs)
    # plt.imsave("images/cone.png", image)
    get_path_and_infos("venn")