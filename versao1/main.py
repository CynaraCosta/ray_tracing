import matplotlib.pyplot as plt
import numpy as np
from geo_objects import Plane, Sphere, Triangle
from render import render

def change_type_input(Type):
    return map(Type, input().split())

def change_type_string(Type, string):
    return map(Type, string.split())

if __name__ == "__main__":

    # getting the info from txt

    v_res, h_res = change_type_input(int)
    square_side, dist = change_type_input(float)
    eye_x, eye_y, eye_z = change_type_input(float)
    look_at_x, look_at_y, look_at_z = change_type_input(float)
    up_x, up_y, up_z = change_type_input(float)
    bg_color_r, bg_color_g, bg_color_b = change_type_input(int)

    how_many_objs = int(input())

    # setting camera
    eye = np.array((eye_x, eye_y, eye_z))
    look_at = np.array((look_at_x, look_at_y, look_at_z))
    up = np.array((up_x, up_y, up_z))
    bg_color = np.array((bg_color_r, bg_color_g, bg_color_b))

    objs = []

    for obj in range(how_many_objs):
        which_info = input()

        # checking if is a plane
        if "/" in which_info:
            color, plane = which_info.split(" / ")
            color_r, color_g, color_b = change_type_string(int, color)
            point_origin_x, point_origin_y, point_origin_z, normal_vector_x, normal_vector_y, normal_vector_z = change_type_string(float, plane) 

            new_plane = Plane((point_origin_x, point_origin_y, point_origin_z), (normal_vector_x, normal_vector_y, normal_vector_z))
            new_plane.set_color((color_r, color_g, color_b))
            objs.append(new_plane)

        # checking if is a sphere 
        elif "*" in which_info:
            color, sphere = which_info.split(" * ")
            color_r, color_g, color_b = change_type_string(int, color)
            center_x, center_y, center_z, radius = change_type_string(float, sphere)

            new_sphere = Sphere((center_x, center_y, center_z), radius)
            new_sphere.set_color((color_r, color_g, color_b))
            objs.append(new_sphere)

        # checking if is a triangle
        elif ">" in which_info:
            color, triangle = which_info.split(" > ")
            color_r, color_g, color_b = change_type_string(int, color)
            point_a_x, point_a_y, point_a_z, point_b_x, point_b_y, point_b_z, point_c_x, point_c_y, point_c_z = change_type_string(float, triangle)

            new_triangle = Triangle((point_a_x, point_a_y, point_a_z), (point_b_x, point_b_y, point_b_z), (point_c_x, point_c_y, point_c_z))
            new_triangle.set_color((color_r, color_g, color_b))
            objs.append(new_triangle)

    # call the render here
    image = render(v_res, h_res, square_side, dist, eye, look_at, up, bg_color, objs)
    plt.imsave("images/baloes.png", image)
    