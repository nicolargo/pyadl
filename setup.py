#!/usr/bin/env python

import os
import sys
import re

from setuptools import setup

with open(os.path.join('pyadl', '__init__.py')) as f:
    version = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M).group(1)


def get_data_files():
    data_files = [
        ('share/doc/pyadl', ['AUTHORS', 'NEWS', 'README.rst'])
    ]

    return data_files


def get_requires():
    requires = []

    if sys.version_info < (2, 7):
        requires += ['argparse']

    return requires


setup(
    name='pyadl',
    version=version,
    description="A simple Python Wrapper for the AMD/ATI ADL lib.",
    long_description=open('README.rst').read(),
    author='Gergo Szabo (aka) hunasdf',
    author_email='szager88@hmail.com',
    url='https://github.com/nicolargo/pyadl',
    license="MIT",
    keywords="amd ati driver wrapper monitoring gpu",
    install_requires=get_requires(),
    extras_require={},
    packages=['pyadl'],
    include_package_data=True,
    data_files=get_data_files(),
    # entry_points={"console_scripts": ["pyadl=pyadl.pyadl:main"]},
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Hardware :: Hardware Drivers',
        'Topic :: System :: Monitoring',
    ]
)
