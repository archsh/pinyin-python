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

from raw_data import PINYIN_WORDS
PINYINS = dict([(x[1],x[0].lower()) for x in PINYIN_WORDS])
def get_pinyin(word):
    if word in PINYINS:
        return PINYINS[word]
    return None

def is_zh(c):
    x = ord (c)
    # Punct & Radicals
    if x >= 0x2e80 and x <= 0x33ff:
        return True
    # Fullwidth Latin Characters
    elif x >= 0xff00 and x <= 0xffef:
        return True
    # CJK Unified Ideographs &
    # CJK Unified Ideographs Extension A
    elif x >= 0x4e00 and x <= 0x9fbb:
        return True
    # CJK Compatibility Ideographs
    elif x >= 0xf900 and x <= 0xfad9:
        return True
    # CJK Unified Ideographs Extension B
    elif x >= 0x20000 and x <= 0x2a6d6:
        return True
    # CJK Compatibility Supplement
    elif x >= 0x2f800 and x <= 0x2fa1d:
        return True
    else:
        return False

def process_phrase(phrase):
    assert isinstance(phrase,unicode)
    output=list()
    cur_zh=None
    cur_py=None
    for c in phrase:
        if not is_zh(c):
            if not cur_py:
                cur_py = c
            else:
                cur_py += c
        else:
            if cur_zh:
                #print 'Get:', cur_zh, 'Py:',cur_py
                output.append((cur_zh, cur_py if cur_py else get_pinyin(cur_zh)))
                cur_py = None
            cur_zh = c
    else:
        if cur_zh:
            #print 'Get:', cur_zh, 'Py:',cur_py
            output.append((cur_zh, cur_py if cur_py else get_pinyin(cur_zh)))
            cur_py = None
    return output
    
    


def load_txt_phrases(filename):
    to_close = False
    if isinstance(filename,(str,unicode)):
        to_close = True
        filename = open(filename,'rU')
    if not isinstance(filename,file):
        raise Exception('Not a file handle.')
    datas = dict()
    for line in filename.readlines():
        line = unicode(line.strip(),'utf8')
        if not line: continue
        #print 'line:>',line
        word,phrases = line.split(u' ',1)
        phrases = [process_phrase(x) for x in filter(lambda x:x, phrases.split(','))]
        if len(word)>1:
            py = word[1:]
        else:
            py = get_pinyin(word[0])
        #print word[0],'(%s)'%py,':',phrases
        if py in datas:
            datas[py].append((word[0],phrases))
        else:
            datas[py]=[(word[0],phrases)]
        #datas.append(((word[0],py),phrases))
    if to_close:
        filename.close()
    return datas


if __name__ == '__!!!!!main__': ### For Dictionary
    import sys, datetime
    if len(sys.argv)>1:
        t1 = datetime.datetime.now()
        dictionary = load_txt_dictionary(sys.argv[1])
        t2 = datetime.datetime.now()
        if len(sys.argv)>2:
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
        
if __name__ == '__main__': ### For Phrases
    import sys, datetime
    if len(sys.argv)>1:
        t1 = datetime.datetime.now()
        dictionary = load_txt_phrases(sys.argv[1])
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
            pass
            #print json.dumps(dictionary,indent=' ')
            
            #write_json(sys.stdout,dictionary)
        
    else:
        print 'Please enter the dictionary filename.'
