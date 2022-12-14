import matplotlib.pyplot as plt
import numpy as np
from geo_objects import Plane, Sphere, Triangle
from render import render
from json_reader import get_path_and_infos

def change_type_input(Type):
    return map(Type, input().split())

def change_type_string(Type, string):
    return map(Type, string.split())

if __name__ == "__main__":
    get_path_and_infos("vidro4")