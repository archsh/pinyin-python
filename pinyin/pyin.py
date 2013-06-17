# -*- coding:utf-8 -*-
import os
def code2unichar(code):
    char = unichr(int(code,16)).encode('utf8')
    #print char,'(%s)'%code
    return char


class Pinyin(object):
    #code
    def __init__(self, filename=None):
        #if filename is None:
        #    filename = os.path.join(os.path.abspath(os.path.dirname(__file__)),'pinyin.dat')
        self._pydata=list()
        self.load(filename)
    
    def load(self, filename=None):
        if filename is None:
            from .pydata import PINYIN_WORDS
            self._pydata = PINYIN_WORDS
        else:
            for line in open(filename):
                line = line.strip()
                zi,pys = line.split('\t',1)
                pys = pys.split(' ')
                row = [code2unichar(zi)]
                row.extend(pys)
                self._pydata.append(row)
    
    def query(self, py):
        def match_pinyin(x):
            for w in x[1:]:
                if w.lower()[:len(py)]==py.lower():
                    return (w,x[0])
            return None
        result = sorted(filter(lambda x: x is not None,map(match_pinyin, self._pydata)),key=lambda x: x[0])
        return map(lambda x:x[1],result)
        #return map(lambda x: x[0], filter(match_pinyin, self._pydata))
            
        
    def gen_data_py(self, filename):
        #f = open(filename,'w')
        f.write('# -*- coding:utf-8 -*-\n')
        f.write('PINYIN_WORDS=(\n')
        for row in self._pydata:
            line=['\t']
            line.append('(')
            line.append(','.join(['"%s"'%x for x in row]))
            line.append('),\n')
            f.write(''.join(line))
        f.write(')\n')
        f.close()
    
