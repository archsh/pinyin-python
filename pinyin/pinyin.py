# -*- coding:utf-8 -*-
import os

class Pinyin(object):
    #code
    def __init__(self, *filename):
        """
        Initialize a Pinyin instance. filename for init with a user word lib filename.
        Use a list if you need multiple filename.
        """
        from data import PINYIN_WORDS
        self._pydata=[list(row) for row in PINYIN_WORDS]
        self._wordlib={}
        #if not filename:
        #    filename = [
        #        os.path.join(os.path.dirname(os.path.abspath(__file__)),'wordlib0.txt'),
        #        os.path.join(os.path.dirname(os.path.abspath(__file__)),'wordlib1.txt'),
        #    ]
        if filename is not None:
            self.load(filename)
    
    def load(self, filename):
        """
        Load user lib data file.
        """
        def matching(x,y=None):
            if not isinstance(x,dict):
                k = x
                x = self._wordlib
                if k in x: x[k]+=1
                else: x[k]=1
            if y:
                if y in x: x[y]+=1
                else: x[y]=1
            return x
        
        if isinstance(filename,file):
            content = filename.read().decode('utf8').strip()
            #print 'length:',len(content)
            if len(content)>10:
                self._wordlib = reduce(matching,list(content))
            new_data = list()
            for row in self._pydata:
                words = row[1:]
                words.sort(key=lambda x:self._wordlib.get(unicode(x,'utf8'),0),reverse=True)
                row = row[:1]+words #row[1:].sort(key=lambda x:self._wordlib.get(x,0))
                new_data.append(row)
            self._pydata = new_data
        elif isinstance(filename,(tuple,list)):
            for fname in filename:
                self.load(fname)
        else:
            f = open(filename)
            self.load(f)

    
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
    
    
    
