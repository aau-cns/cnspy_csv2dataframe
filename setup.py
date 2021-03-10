#!/usr/bin/env python

from distutils.core import setup

setup(name='csv2dataframe',
      version='1.0',
      description='Python Distribution Utilities',
      author='Roland Jung',
      author_email='roland.jung@aau.at',
      url='https://gitlab.aau.at/aau-cns/py3_pkgs/csv2dataframe/',
      packages=['distutils', 'distutils.command', 'numpy', 'pandas', 'numpy_utils', 'spatial_csv_formats'],
     )
