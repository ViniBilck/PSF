from psf.static import *
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.modeling import models, fitting


class PSF(object):
    def __init__(self, galaxy_file: str, stars_coordinates_file: str = '', delta_axes: int = 20):
        self.delta_axes = delta_axes
        self.galaxy_file_data = fits.getdata(galaxy_file)
        if stars_coordinates_file:
            self.stars_coordinates = get_stars_coordinates(stars_coordinates_file)
        else:
            pass

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

    def do_averaging(self, plot=False):
        get_psf = self.do_psf()
        all_psf = np.array([psf[0] for psf in get_psf])
        print(np.sum(all_psf))
        average = np.mean(all_psf, axis=0)
        if plot:
            plt.imshow(average, origin="lower")
            plt.show()
        return average

    def do_norm(self, plot=True):
        get_average = self.do_averaging()
        norm_const = 1 / np.max(get_average)
        norm = get_average * norm_const
        if plot:
            plt.imshow(norm, origin="lower")
            plt.show()
        return norm

    def find_saturated_stars(self, condition_saturation: float, exclusion_radius: float, plot=True, vmax=0.7):
        bool_matrix = (self.galaxy_file_data > condition_saturation)
        mask_matrix = roll_circular(bool_matrix, exclusion_radius)
        if plot:
            fig, axs = plt.subplots(1, 2, figsize=(9, 3), sharey=True)
            axs[0].imshow(mask_matrix, origin="lower")
            axs[1].imshow(self.galaxy_file_data * (~mask_matrix), vmax=vmax, origin="lower")
            plt.show()
        return mask_matrix

    def remove_galaxy_mask(self, galaxy_coord: tuple, pixel_size=19):
        mask = np.full(self.galaxy_file_data.shape[:2], False)
        y, x = galaxy_coord
        mask[x - pixel_size:x + pixel_size, y - pixel_size:y + pixel_size] = True
        return mask

    def remove_saturated_objects(self, galaxy_coord: tuple, pixel_size: int, condition_saturation: float,
                                 exclusion_radius: float, plot=True):
        saturated_stars = self.find_saturated_stars(condition_saturation, exclusion_radius, plot=False)
        mask = self.remove_galaxy_mask(galaxy_coord, pixel_size=pixel_size)
        new_data = self.galaxy_file_data * (~saturated_stars) * (~mask)
        if plot:
            fig, axs = plt.subplots(1, 1, figsize=(9, 3), sharey=True)
            axs.imshow(new_data, origin="lower", vmax=0.7)
            plt.show()
        return new_data
