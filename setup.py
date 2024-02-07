from numpy.distutils.core import setup

package_data = {
    'PSF': [
        'psf/*',
    ]
}

setup(
    name='PSF',
    python_requires='>=3.7',
    version="0.1",
    packages=['psf'],
    package_data=package_data,
    scripts=['bin/coordinates', 'bin/createPSF', 'bin/plot_residuals', 'bin/plot_file', 'bin/plot_star'],
    description="Script to create a average psf image",
    author="Vinicius Lourival Bilck",
    author_email="bilck.vinicius1998@gmail.com",
    url='https://github.com/ViniBilck/PSF',
    platform='Linux',
    license="MIT License",
    classifiers=['Programming Language :: Python :: 3.11'],
)