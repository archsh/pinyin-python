# -*- coding:utf-8 -*-
import os
def code2unichar(code):
    char = unichr(int(code,16)).encode('utf8')
    #print char,'(%s)'%code
    return char

def raw_to_optimized(raw_data,filename=None):
    """
    Convert raw data to optimized data.
    """
    import sys, datetime
    assert raw_data
    WORDS={}
    for row in raw_data:
        py = row[0][:-1]
        if py in WORDS:
            WORDS[py].append(row[1])
        else:
            WORDS[py]=[row[1]]
    if filename:
        f = open(filename,'w')
        lines = list()
        for k,v in WORDS.items():
            lines.append([k]+v)
        lines.sort(key=lambda x:x[0])
        f.write('# -*- coding:utf-8 -*-\n')
        f.write('PINYIN_WORDS=(\n')
        for row in lines:
            line=['\t']
            line.append('(')
            line.append(','.join(['"%s"'%x for x in row]))
            line.append('),\n')
            f.write(''.join(line))
        f.write(')\n')
        f.close()
    else:
        for k,v in WORDS.items():
            print k,':',len(v)  


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
        if not filename:
            filename = [
                os.path.join(os.path.dirname(os.path.abspath(__file__)),'wordlib0.txt'),
                os.path.join(os.path.dirname(os.path.abspath(__file__)),'wordlib1.txt'),
            ]
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

    
    def query(self, py,cross_sort=False):
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
        #t1 = datetime.datetime.now()
        result = map(lambda x: x[1:],filter(match_pinyin,self._pydata))
        #print result
        #t2 = datetime.datetime.now()
        #sorted(filter(lambda x: x is not None,map(match_pinyin, self._pydata)),key=lambda x: x[0])
        result = reduce(ext,result) if len(result)>1 else ext(result[0]) if result else []
        #t3 = datetime.datetime.now()
        if cross_sort:
            result.sort(key=lambda x:self._wordlib.get(unicode(x,'utf8'),0),reverse=True)
        #t4 = datetime.datetime.now()
        #print 'query> t2-t1:',t2-t1
        #print 'query> t3-t2:',t3-t2
        #print 'query> t4-t3:',t4-t3
        return result
        #return map(lambda x: x[0], filter(match_pinyin, self._pydata))
    
if __name__ == '__##main__':
    import sys, datetime
    t1 = datetime.datetime.now()
    py = Pinyin()
    t2 = datetime.datetime.now()
    if len(sys.argv)>1:
        ret = py.query(sys.argv[1])
    else:
        ret = py.query('dang')
    t3 = datetime.datetime.now()
    print len(ret)
    
    for x in ret:
        print x,
    print ''
    print 't2-t1:',t2-t1
    print 't3-t2:',t3-t2

if __name__ == '__main__':
    import sys
    from raw_data import PINYIN_WORDS
    raw_to_optimized(PINYIN_WORDS,sys.argv[1] if len(sys.argv)>1 else None)
    
    
    
