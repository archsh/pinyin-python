# -*- coding:utf-8 -*-
import os
def code2unichar(code):
    char = unichr(int(code,16)).encode('utf8')
    #print char,'(%s)'%code
    return char

class Pinyin(object):
    #code
    def __init__(self, filename=None):
        """
        Initialize a Pinyin instance. filename for init with a user lib filename.
        """
        from data import PINYIN_WORDS
        self._pydata=PINYIN_WORDS
        if filename is not None:
            self.load(filename)
    
    def load(self, filename):
        '''
        Load user lib data file.
        '''
        pass
    
    def query(self, py):
        import datetime
        py = py.upper()
        def match_pinyin(x):
            if x[0][:len(py)]==py:
                return True
            return False
        def ext(x,y=None):
            if not isinstance(x,list):
                x = list(x[1:])
            if y:
                x.extend(y[1:])
            return x
        #t1 = datetime.datetime.now()
        result = filter(match_pinyin,self._pydata)
        #print result
        #t2 = datetime.datetime.now()
        #sorted(filter(lambda x: x is not None,map(match_pinyin, self._pydata)),key=lambda x: x[0])
        result = reduce(ext,result) if len(result)>1 else ext(result[0]) if result else []
        #t3 = datetime.datetime.now()
        #print 'query> t2-t1:',t2-t1
        #print 'query> t3-t2:',t3-t2
        return result
        #return map(lambda x: x[0], filter(match_pinyin, self._pydata))
    
if __name__ == '__main__':
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

if __name__ == '__TmainT__':
    import sys, datetime
    from pydata import PINYIN_WORDS
    WORDS={}
    for row in PINYIN_WORDS:
        py = row[0][:-1]
        if py in WORDS:
            WORDS[py].append(row[1])
        else:
            WORDS[py]=[row[1]]
    if len(sys.argv)>1:
        f = open(sys.argv[1],'w')
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
    
    
    
