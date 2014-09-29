#!/usr/bin/env python

from distutils.core import setup
import os
setup(name='ponda',
      version='0.0.1',
      description='PO File Parser',
      packages=['ponda', 'ponda.scripts'],
      scripts=['scripts/pofile2csv'],
      package_dir = {'': os.path.dirname(__file__)}
     )
