from astropy.modeling import models, fitting
from astropy.io import fits
import numpy as np


class PSF(object):
    def __init__(self, galaxy_file: str, stars_coordinates: str, delta_axes: float = 20.0):
        self.stars_coordinates_file = stars_coordinates
        self.delta_axes = delta_axes
        self.galaxy_file = galaxy_file

    def get_stars_coordinates(self):
        with open(self.stars_coordinates_file) as coordinate_list:
            text_read = coordinate_list.read()
        return text_read

    def get_stars(self):
        return fits.getdata(self.galaxy_file)

    def do_cuts(self):
        return 0

    def do_fits(self):
        return 0

    def do_psf(self):
        return 0
