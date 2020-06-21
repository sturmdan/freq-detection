#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 15:55:59 2020

@author: dansturm
"""


from setuptools import setup
from Cython.Build import cythonize

setup(
      name = 'Attempt to create vector c code',
      ext_modules = cythonize("vectors.pyx"),
      zip_safe = False,
)