import copy
import numpy as np


def get_stars_coordinates(star_coordinates_file: str) -> list[list[str]]:
    with open(star_coordinates_file) as coordinate_list:
        coordinates = [line.strip() for line in coordinate_list]
        points = [point.split(",") for point in coordinates]
    return points


def roll_circular(boolean_condition_matrix, radius):
    z = copy.deepcopy(boolean_condition_matrix)
    for i in range(-radius, radius + 1):
        for j in range(-radius, radius + 1):
            if i ** 2 + j ** 2 <= radius ** 2:
                z |= np.roll(boolean_condition_matrix, (i, j), axis=(0, 1))
    return z
