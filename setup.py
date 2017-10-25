# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
# from distutils.core import setup


setup(
  name='namesex',
  packages = ['namesex'],
  version = '0.0.7', 
  description='Gender Classification by Chinese Name',
  author = 'HSIN-MIN LU, YU-LUN LI, CHI-YU LIN',
  author_email = 'evan860126@gmail.com',
  keywords = ['name,gender'],
  install_requires=[
  	'gensim',
  	'sklearn',
  ],
  url = 'https://github.com/EvanYo25/namesex-1',
  download_url = 'https://github.com/EvanYo25/namesex-1',
  include_package_data=True
)