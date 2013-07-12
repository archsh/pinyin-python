# -*- coding:utf-8 -*-
import os
try:
    import simplejson as json
except Exception:
    import json
from dictionary import PINYIN_DICTIONARY

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
            self.dictionary = None
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
    
    

    
    def query(self, py,cross_sort=False,remove_dup=False):
        import datetime
        py = py.upper()
        def match_pinyin(x):
            if x[0][:len(py)]==py:
                return True
            return False
        def ext(x,y=None):
            if not isinstance(x,list):
                x = list(x)
            if y:
                x.extend(y)
            return x
        def remove_dup(x,y):
            if not isinstance(x,list):
                x=[x]
            if y not in x:
                x.append(y)
            return x
        
        #t1 = datetime.datetime.now()
        result = map(lambda x: x[1:],filter(match_pinyin,self._pydata))
        #print result
        #t2 = datetime.datetime.now()
        #sorted(filter(lambda x: x is not None,map(match_pinyin, self._pydata)),key=lambda x: x[0])
        ret = reduce(ext,result) if len(result)>1 else ext(result[0]) if result else []
        result = reduce(remove_dup,ret) if len(ret)>1 else ret if remove_dup else ret
        #for x in ret:
        #    if x not in result:
        #        result.append(x)
        #t3 = datetime.datetime.now()
        if cross_sort:
            result.sort(key=lambda x:self._wordlib.get(unicode(x,'utf8'),0),reverse=True)
        #t4 = datetime.datetime.now()
        #print 'query> t2-t1:',t2-t1
        #print 'query> t3-t2:',t3-t2
        #print 'query> t4-t3:',t4-t3
        return result
        #return map(lambda x: x[0], filter(match_pinyin, self._pydata))
    
if __name__ == '__main__':
    import sys, datetime
    t1 = datetime.datetime.now()
    py = Pinyin('../test/wordlib0.txt','../test/wordlib1.txt')
    t2 = datetime.datetime.now()
    if len(sys.argv)>1:
        ret = py.query(sys.argv[1],True,True)
    else:
        ret = py.query('dang',True,True)
    t3 = datetime.datetime.now()
    print len(ret)
    
    for x in ret:
        print x,
    print ''
    print 't2-t1:',t2-t1
    print 't3-t2:',t3-t2

if __name__ == '__##main__':
    import sys
    from raw_data import PINYIN_WORDS
    raw_to_optimized(PINYIN_WORDS,sys.argv[1] if len(sys.argv)>1 else None)
    
    
    
