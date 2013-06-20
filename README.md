# pinyin-python

A simple pinyin engine for Python.

Usage:

  import pinyin
  
  py = Pinyin('wordlib1.txt','wordlib2.txt',)
  
  for w in py.query('tian'): print w
