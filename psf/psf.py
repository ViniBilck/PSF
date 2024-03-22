import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
from astropy.modeling import models, fitting


def get_stars_coordinates(star_coordinates_file: str) -> list[list[str]]:
    with open(star_coordinates_file) as coordinate_list:
        coordinates = [line.strip() for line in coordinate_list]
        points = [point.split(",") for point in coordinates]
    return points


class PSF(object):
    def __init__(self, galaxy_file: str, stars_coordinates_file: str, delta_axes: int = 20):
        self.delta_axes = delta_axes
        self.galaxy_file_data = fits.getdata(galaxy_file)
        self.stars_coordinates = get_stars_coordinates(stars_coordinates_file)

    def get_stars(self):
        stars_data = []
        for star in self.stars_coordinates:
            x, y = int(round(float(star[0]))), int(round(float(star[1])))
            fits_data = self.galaxy_file_data[y - self.delta_axes: y + self.delta_axes,
                                              x - self.delta_axes: x + self.delta_axes]
            stars_data.append(fits_data)
        return stars_data

    def do_psf(self):
        print("Start doing PSF using moffat2D")
        moffat2d_fits = []
        for stars_data in self.get_stars():
            g = models.Moffat2D(amplitude=stars_data.max(), x_0=0.0, y_0=0.0)
            y, x = np.indices(stars_data.shape)
            y -= self.delta_axes
            x -= self.delta_axes
            fit = fitting.LevMarLSQFitter()
            p = fit(g, x, y, stars_data)
            print(f"Amplitude={p.parameters[0]}, "
                  f"x_0={p.parameters[1]}, "
                  f"y_0={p.parameters[2]}, "
                  f"Gamma={p.parameters[3]}, "
                  f"Alpha={p.parameters[4]}")
            moffat2d_fits.append([p(x, y), p.parameters])
        return moffat2d_fits

    def get_file_plot(self, vmax: float = 10.0):
        fig, ax = plt.subplots(1, 1)
        ax.imshow(self.galaxy_file_data, vmax=vmax, origin="lower")
        plt.show()

    def get_stars_plot(self):
        nstars = len(self.stars_coordinates)
        fig, ax = plt.subplots(1, nstars)
        for index, star in enumerate(self.get_stars()):
            ax[index].imshow(star, origin="lower")
        plt.show()

    def get_residuals_plot(self):
        nstars = len(self.stars_coordinates)
        fig, ax = plt.subplots(1, nstars)
        count = 0
        for star, psf in zip(self.get_stars(), self.do_psf()):
            ax[count].imshow(star - psf[0], origin="lower")
            count += 1
        plt.show()

    def do_averaging(self):
        get_psf = self.do_psf()
        all_psf = np.array([psf[0] for psf in get_psf])
        print(np.sum(all_psf))
        plt.imshow(np.mean(all_psf, axis=0), origin="lower")
        plt.show()


