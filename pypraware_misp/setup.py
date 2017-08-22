"""A setuptools based setup module.(Pypa)
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pypraware',

    version='0.1.4',

    description='Privacy aware library for MISP module',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/MISP/misp-privacy-aware-exchange',

    # Author details
    author='Charles Jacquet',
    author_email='charles.jacquet7@gmail.com',

    # Choose your license
    license='GNU Affero General Public License v3.0',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    # What does your project relate to?
    keywords='MISP module privacy',

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    packages=["pypraware_crypto", "pypraware_normalize"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['configparser', 'cryptography', 'bcrypt', 'bitarray', 'urllib', 'url_normalize', 'ipaddress'],

)

