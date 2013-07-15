# pinyin-python

A simple pinyin engine for Python.

Usage:

    >>> import pinyin
  
    >>> py = pinyin.Pinyin()
    >>> py.load_phrases(filename="datas/phrase.json")
    >>> pys,words = py.query('yipinby')
    >>> print pys
    ['yi', 'pin', 'b', 'y']
    >>> for w in words: print '>',w
    ...
    > 一品鲍鱼
    > 一
    > 以
    > 意
    > 已
    > 义
    > 议
    > 医
    > 易
    > 衣
    > 艺
    > 依
    > 译
    > 移
    > 异
