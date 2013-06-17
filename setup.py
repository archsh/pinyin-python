# -*- coding:utf-8 -*-
import sys
from distutils.core import setup
from pinyin import __version__

setup(name='pinyin-python',
      version=__version__,
      description='A small and simple Chinese pinyin engine for Python.',
      long_description=open("README.md").read(),
      author='Mingcai SHEN',
      author_email='archsh@gmail.com',
      packages=['pinyin'],
      package_dir={'pinyin': 'pinyin'},
      package_data={'pinyin': ['pinyin.dat']},
      license="Public domain",
      platforms=["any"],
      url='https://github.com/archsh/pinyin-python')
