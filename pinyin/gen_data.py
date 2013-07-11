# -*- coding:utf-8 -*-
import os
import simplejson as json
def load_txt_dictionary(filename):
    to_close = False
    if isinstance(filename,(str,unicode)):
        to_close = True
        filename = open(filename,'rU')
    if not isinstance(filename,file):
        raise Exception('Not a file handle.')
    datas = dict()
    pys   = list()
    wnums = 0
    for line in filename.readlines():
        line = unicode(line.strip(),'utf8')
        #print 'line:>',line
        xx = line.split(' ',1)
        if len(xx)!=2:
            continue
        py = xx[0]
        words = [x for x in xx[1]]
        if py in datas:
            datas[py].extend(words)
        else:
            datas[py]=words
            pys.append(py)
        #print py,':',len(words)
        wnums += len(words)
        #datas.append((py,words))
    print 'PY Length:', len(datas.keys())
    print 'Total Words1:',wnums
    if to_close:
        filename.close()
    ret = list()
    total_words=0
    for py in pys:
        total_words += len(datas[py])
        ret.append((py, [(w,0) for w in datas[py]]))
    print 'Total Words2:',total_words
    return ret
    
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

def write_data_python(filename,datas):
    assert datas
    to_close = False
    if isinstance(filename,(str,unicode)):
        to_close = True
        filename = open(filename,'w')
    if not isinstance(filename,file):
        raise Exception('Not a file handle.')
    filename.write("""# -*- coding:utf-8 -*-
PINYIN_WORDS=(\n""")
    for py,words in datas:
        line = u'("%s", %s),\n'%(py.upper(), u','.join([u'"%s"'%x[0] for x in words]))
        filename.write(line.encode('utf8'))
    filename.write(")\n")
    filename.close()
    


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

def load_txt_phrases(filename):
    pass


if __name__ == '__main__':
    import sys, datetime
    from data import PINYIN_WORDS
    if len(sys.argv)>1:
        t1 = datetime.datetime.now()
        dictionary = load_txt_dictionary(sys.argv[1])
        t2 = datetime.datetime.now()
        if len(sys.argv)>2:
            #f = open(sys.argv[2],'w')
            #for py,words in dictionary:
            #    line = u'%s %s\n'%(py, u''.join([x[0] for x in words]))
            #    f.write(line.encode('utf8'))
            #f.close()
            #write_data_python(sys.argv[2],dictionary)
            write_json(sys.argv[2],dictionary)
            t3 = datetime.datetime.now()
            dictionary = load_json(filename=sys.argv[2])
            t4 = datetime.datetime.now()
            print 't2-t1:', t2-t1
            print 't3-t2:', t3-t2
            print 't4-t3:', t4-t3
            #for py,words in dictionary:
            #    words = sorted(words,key=lambda x:x[1])
            #    print py,':',
            #    for w,n in words:
            #        print w,'(%d)'%n,
            #    print '\n'
        else:
            for py,words in dictionary:
                print py, u''.join([x[0] for x in words])
            
            #write_json(sys.stdout,dictionary)
        
    else:
        print 'Please enter the dictionary filename.'
        

