from typing import List

from astropy.modeling import models, fitting
from astropy.io import fits
import numpy as np


class PSF(object):
    def __init__(self, galaxy_file: str, stars_coordinates_file: str, delta_axes: float = 20.0):
        self.delta_axes = delta_axes
        self.galaxy_file_data = fits.getdata(galaxy_file)
        self.stars_coordinates = self.get_stars_coordinates(stars_coordinates_file)

    def get_stars_coordinates(self, star_coordinates_file: str) -> list[list[str]]:
        with open(star_coordinates_file) as coordinate_list:
            coordinates = [line.strip() for line in coordinate_list]
            points = [point.split(",") for point in coordinates]
        return points

    def get_stars(self):
        return 0

    def do_cuts(self):
        return 0

    def do_fits(self):
        return 0

    def do_psf(self):
        return 0
