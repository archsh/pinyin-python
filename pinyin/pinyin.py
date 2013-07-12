# -*- coding:utf-8 -*-
import os
try:
    import simplejson as json
except Exception:
    import json
from dictionary import PINYIN_DICTIONARY

PY_SHENGMU = ("b","p","m","f","d","t","n","l","g","k","h","j","q","x","zh","ch","sh","r","z","c","s","y","w")
PY_YUNMU   = ("a","o","e","ai","ei","ao","ou","an","en","ang","eng","ong","i","ia","ie","iao","iou","ian","in","iang","iong","u","ua","uai","uan","uen","uang","ueng","v")

def load_json(filename=None,content=None):
    to_close = False
    if filename is not None:
        if isinstance(filename,(str,unicode)):
            to_close = True
            filename = open(filename,'r')
        if not isinstance(filename,file):
            raise Exception('Not a file handle.')
        try:
            datas = json.loads(filename.read())
        except Exception,e:
            print 'Load JSON failed:',e
            datas = []
        if to_close:
            filename.close()
    elif content is not None:
        try:
            datas = json.loads(content)
        except Exception,e:
            print 'Load JSON failed:',e
            datas = []
    else:
        raise Exception('Neither filename or content is available!')
    return datas

def write_json(filename,datas):
    assert datas
    to_close = False
    if isinstance(filename,(str,unicode)):
        to_close = True
        filename = open(filename,'w')
    if not isinstance(filename,file):
        raise Exception('Not a file handle.')
    filename.write(json.dumps(datas))
    if to_close:
        filename.close()

class Pinyin(object):
    #code
    def __init__(self, dictionary=None):
        """
        Initialize a Pinyin instance.
        Parameter:
        @dictionary: a dict of dictionary format or a JSON format string.
        """
        if dictionary:
            if isinstance(dictionary,dict):
                self.dictionary = dictionary
            else:
                try:
                    self.dictionary = json.loads(dictionary)
                except Exception,e:
                    print 'Warning: Invalid JSON format!',e
                    self.dictionary = None
        else:
            self.dictionary = PINYIN_DICTIONARY
        self.phrases = None
    
    def load_dictionary(self, filename=None, content=None):
        """
        Load dictionary from a JSON formated file(filename) or string(content).
        Parameters:
        @filename: a string of filename and path or a file object.
        @content: a string of JSON.
        """
        self.dictionary = load_json(filename=filename,content=content)
    
    
    def load_phrases(self, filename=None,content=None):
        """
        Load phrases from a JSON formated file(filename) or string(content).
        Parameters:
        @filename: a string of filename and path or a file object.
        @content: a string of JSON.
        """
        self.phrases = load_json(filename=filename,content=content)
    
    def save_dictionary(self, filename):
        """
        Save current disctionary to a file with JSON format.
        Parameters:
        @filename: a string of filename and path or a file object.
        """
        write_json(filename,self.dictionary)
    
    def save_phrases(self, filename):
        """
        Save current phrases to a file with JSON format.
        Parameters:
        @filename: a string of filename and path or a file object.
        """
        write_json(filename,self.phrases)
    
    def validate_dictionary(self):
        if not self.dictionary:
            raise Exception('Please load dictionary or make sure your dictionary is valid!')
    
    
    def pinyin_split(self,pystr):
        '''
        pinyin_split: split a given pinyin string to a list of seperated pinyin.
        '''
        def match_pinyin(s):
            if filter(lambda x: x.startswith(s),self.dictionary.keys()):
                return True
            return False
        assert pystr
        self.validate_dictionary()
        pystr = pystr.encode('ascii')
        result = list()#(pystr)#.split('')
        last_ch = None
        for c in pystr:
            if not last_ch:
                last_ch = c
                continue
            if match_pinyin(last_ch+c):
                last_ch += c
                continue
            else:
                result.append(last_ch)
                last_ch = c
        else:
            if last_ch:
                result.append(last_ch)
        return result
    
    def fetch_phrases(self, pys,selected=None):
        assert pys
        def match_pinyin(pys,pinyinfull):
            for p,pp in map(None,pys,pinyinfull.split('-')):
                if not p:
                    break;
                if not pp or not pp.startswith(p):
                    return False
            print 'Matched: %s <-> %s'%('-'.join(pys),pinyinfull)
            return True
        result = []
        if not self.phrases:
            return []
        for pk in sorted(filter(lambda x: x.startswith(pys[0]),self.phrases.keys())):
            if match_pinyin(pys,pk):
                if not selected:
                    result.extend(self.phrases[pk])
                else:
                    result.extend(filter(lambda x: x.startswith(selected),self.phrases[pk]))
        return result
            
        
    def fetch_word(self, py):
        assert py
        def remove_dup(x,y):
            if not isinstance(x,list):
                x=[x]
            if y not in x:
                x.append(y)
            return x
        def _do_fetch(piny):
            if piny in self.dictionary.keys():
                return map(lambda k: k[0], sorted(self.dictionary[piny].items(),key=lambda x:x[1], reverse=True))
            else:
                result = list()
                for k in filter(lambda x: x.startswith(piny),sorted(self.dictionary.keys())):
                    result.extend(_do_fetch(k))
                return result
        result = _do_fetch(py)
        result = reduce(remove_dup,result) if len(result)> 1 else result
        return result
    
    def query(self, py,index=-1,selected=None):
        if not py:
            return []
        pys = self.pinyin_split(py)
        if len(pys)<1:
            return []
        elif len(pys)==1:
            return self.fetch_word(pys[0])
        else:
            phrases = self.fetch_phrases(pys,selected=None)
            if index>=len(pys) or index<0:
                index = 0
            words = self.fetch_word(pys[index])
            return phrases + words
    
    
    
