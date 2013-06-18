# pinyin-python

A simple pinyin engine for Python.

Usage:

>>> import pinyin
>>> py = Pinyin() # You can initialize with your words lib in UTF-8 text format.
>>> for w in py.query('tian'): print w
