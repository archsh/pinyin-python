# -*- coding:utf-8 -*-
import os, datetime, re
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
        @dictionary: a dict of dictionary format or a JSON format string. A default dictionary will be used if this is None.
        """
        if dictionary:
            if isinstance(dictionary,dict):
                self.dictionary = dictionary
            else:
                try:
                    self.dictionary = json.loads(dictionary)
                    self.resort_dictionary(self.dictionary)
                except Exception,e:
                    print 'Warning: Invalid JSON format!',e
                    self.dictionary = None
        else:
            self.dictionary = PINYIN_DICTIONARY
            self.resort_dictionary(self.dictionary)
        self.phrases = None
        
    def resort_dictionary(self, dictionary, py_optimized=None, wd_optimized=None):
        assert isinstance(dictionary,dict)
        def _m(x,y):
            if not isinstance(x,list):
                x=list()
            if isinstance(y,list):
                x.extend(y)
            return x
        self.dictionary_keys = set(map(lambda x:x[0], reduce(_m,self.dictionary.values())))

    def resort_phrases(self, phrases):
        words = {}
        if phrases:
            self.phrases_keys = sorted(phrases.keys())
            #self.phrases_keys_dict = dict([(x,tuple(x.split('-'))) for x in self.phrases_keys])
            for k,p in phrases.items():
                pys = k.split('-')
                for ws in p:
                    for py,w in map(None,pys,ws):
                        if w in words:
                            words[w]['sort']+=1
                        else:
                            words[w]={'py':py,'sort':1}
            words = sorted(map(lambda x: (x[0],x[1]['py'],x[1]['sort']),words.items()),key=lambda x:x[2],reverse=False)
            for w,p,s in words:
                if p[0] not in self.dictionary:
                    continue
                l = [p,w]
                if l in self.dictionary[p[0]]:
                    self.dictionary[p[0]].remove(l)
                    self.dictionary[p[0]].insert(0,l)
            if False:
                opt_dictionary = dict()
                pys_dictionary = dict()
                for k,v in phrases.items():
                    for py in k.split('-'):
                        if py in pys_dictionary:
                            pys_dictionary[py]+=1
                        else:
                            pys_dictionary[py]=1
                    for p in v:
                        for w in p:
                            if w in opt_dictionary:
                                opt_dictionary[w]+=1
                            else:
                                opt_dictionary[w]=1000
                #self.resort_dictionary(self.dictionary,pys_dictionary,opt_dictionary)
            
        else:
            self.phrases_keys = []
            #self.phrases_keys_dict = dict()
    
    
    def load_dictionary(self, filename=None, content=None):
        """
        Load dictionary from a JSON formated file(filename) or string(content).
        Parameters:
        @filename: a string of filename and path or a file object.
        @content: a string of JSON.
        """
        self.dictionary = load_json(filename=filename,content=content)
        self.resort_dictionary(self.dictionary)
    
    
    def load_phrases(self, filename=None,content=None):
        """
        Load phrases from a JSON formated file(filename) or string(content).
        Parameters:
        @filename: a string of filename and path or a file object.
        @content: a string of JSON.
        """
        self.phrases = load_json(filename=filename,content=content)
        self.resort_phrases(self.phrases)
        
    
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
            if filter(lambda x: x.startswith(s),self.dictionary_keys):
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
        t1 = datetime.datetime.now()
        def match_pinyin(pys,pinyinfull):
            for p,pp in map(None,pys,pinyinfull):
                if not p:
                    break;
                if p in self.dictionary_keys and p!=pp:
                    return False
                if not pp or not pp.startswith(p):
                    return False
            #print 'Matched: %s <-> %s'%('-'.join(pys),pinyinfull)
            return True
        result = []
        if not self.phrases:
            return []
        regx = r'\-'.join([r'%s[a-z]*'%x for x in pys])+r'$'#+r'.*'
        pt = re.compile(regx)
        for pk in filter(lambda x: x.startswith(pys[0]),self.phrases_keys):
            if pt.match(pk):
                if not selected:
                    result.extend(self.phrases[pk])
                else:
                    result.extend(map(lambda x:x[len(selected):],filter(lambda x: x.startswith(selected),self.phrases[pk])))
        t2 = datetime.datetime.now()
        print 'fetch_phrases:',t2-t1
        return result
            
        
    def fetch_word(self, py):
        assert py
        t1 = datetime.datetime.now()
        def remove_dup(x,y):
            if not isinstance(x,list):
                x=[x]
            if y not in x:
                x.append(y)
            return x

        def _do_fetch(piny):
            if piny[0] in self.dictionary:
                for x in map(lambda x:x[1], filter(lambda x:x[0].startswith(piny),self.dictionary[piny[0]])):
                    yield x
    
        result = _do_fetch(py)
        result = reduce(remove_dup,result,[]) # if len(result)> 1 else result
        t2 = datetime.datetime.now()
        print 'fetch_word:',t2-t1
        return result
    
    def query(self, py,index=-1,selected=None):
        """
        query: get the words according to the pinyin supplied.
        Parameters:
        @py: the pinyin inputed.
        @index: get the word from index, -1 means full phrase first. otherwize, return words only.
        @selected: the selected word(s) from the begin of a phrase, this will filter the return phrases.
        Return: A tuple with pinyin in a list and the queried phrases and words.
        """
        if not py:
            return [],[]
        pys = self.pinyin_split(py)
        if len(pys)<1:
            return [],[]
        elif len(pys)==1:
            return pys, self.fetch_word(pys[0])
        else:
            if index>=len(pys):
                index = -1
            phrases = self.fetch_phrases(pys,selected=selected)
            words = self.fetch_word(pys[0 if index<0 else index])
            return pys, phrases + words if len(pys)>1 else words+phrases
    
    def report(self, pys, words):
        """
        report: send the result(user selected words or phrases) for a pinyin, this will affect to the sort of the phrases or words.
        Parameters:
        @pys: the pinyin in list format returned by query.
        @words: the words selected by user.
        Return: None
        """
        if len(pys)<1 or len(words)<1:
            return
        print 'Reported:','-'.join(pys),words
        fullpys = list()
        idx=0
        for p,w in map(None,pys,words):
            if p[0] not in self.dictionary:
                return
            l = filter(lambda x:x[0].startswith(p) and x[1]==w, self.dictionary[p[0]])
            if not l:
                return
            l = min(l,key=lambda x:x[0])
            fullpys.append(l[0])
            self.dictionary[p[0]].remove(l)
            self.dictionary[p[0]].insert(0,l)
            
        if len(fullpys)>1:
            fullpys = '-'.join(fullpys)
            if fullpys in self.phrases:
                if words in self.phrases[fullpys]:
                    self.phrases[fullpys].remove(words)
                    self.phrases[fullpys].insert(0,words)
                else:
                    self.phrases[fullpys].insert(0,words)
                self.phrases_keys.remove(fullpys)
            else:
                self.phrases[fullpys]=[words]
            self.phrases_keys.insert(0,fullpys)
            

