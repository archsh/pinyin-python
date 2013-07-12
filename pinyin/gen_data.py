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
    ret = dict()
    total_words=0
    for py in pys:
        total_words += len(datas[py])
        pywords = {}
        idx = 0
        length = len(datas[py])
        for w in datas[py]:
            pywords[w]=length-idx
            idx+=1
        
        ret[py]=pywords
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
    


def write_json(filename,datas,indent=None):
    assert datas
    to_close = False
    if isinstance(filename,(str,unicode)):
        to_close = True
        filename = open(filename,'w')
    if not isinstance(filename,file):
        raise Exception('Not a file handle.')
    filename.write(json.dumps(datas,indent=indent))
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

def process_phrase(py,word,phrase):
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
    return py+'-'+('-'.join(map(lambda x:x[1],output))),word+(''.join(map(lambda x:x[0],output)))
    
    


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
        if len(word)>1:
            py = word[1:]
        else:
            py = get_pinyin(word[0])
        for x in filter(lambda x:x, phrases.split(',')):
            pys,words = process_phrase(py,word[0],x)
            if pys in datas:
                datas[pys].append(words)
            else:
                datas[pys]=[words]
    if to_close:
        filename.close()
    return datas


import sys, datetime

def process_dictionary(txtfile,jsonfile=None,jsonindent=None): ### For Dictionary
    assert txtfile
    t1 = datetime.datetime.now()
    dictionary = load_txt_dictionary(txtfile)
    t2 = datetime.datetime.now()
    if jsonfile:
        #write_data_python(sys.argv[2],dictionary)
        write_json(jsonfile,dictionary,indent=jsonindent)
        t3 = datetime.datetime.now()
        dictionary = load_json(filename=jsonfile)
        t4 = datetime.datetime.now()
        print 't2-t1:', t2-t1
        print 't3-t2:', t3-t2
        print 't4-t3:', t4-t3
    else:
        for py,words in dictionary:
            print py, u''.join([x[0] for x in words])


def process_phrases(txtfile,jsonfile=None,jsonindent=None): ### For Phrases
    assert txtfile
    t1 = datetime.datetime.now()
    phrases = load_txt_phrases(txtfile)
    t2 = datetime.datetime.now()
    if jsonfile:
        #f = open(sys.argv[2],'w')
        #for py,words in dictionary:
        #    line = u'%s %s\n'%(py, u''.join([x[0] for x in words]))
        #    f.write(line.encode('utf8'))
        #f.close()
        #write_data_python(sys.argv[2],dictionary)
        write_json(jsonfile,phrases,indent=jsonindent)
        t3 = datetime.datetime.now()
        phrases = load_json(filename=jsonfile)
        t4 = datetime.datetime.now()
        print 't2-t1:', t2-t1
        print 't3-t2:', t3-t2
        print 't4-t3:', t4-t3
        for k,v in phrases.items():
            print k,':', u','.join(v)        
    else:
        pass
        #print json.dumps(dictionary,indent=' ')

if __name__ == '__main__':
    indent = ' '
    if len(sys.argv)<3:
        print 'Usage: gen_data.py dictionary|phrase txt_filename [json_output_filename]'
        sys.exit(1)
    if sys.argv[1]=='dictionary':
        process_dictionary(sys.argv[2], jsonfile=None if len(sys.argv)<4 else sys.argv[3], jsonindent=indent)
    elif sys.argv[1]=='phrase':
        process_phrases(sys.argv[2], jsonfile=None if len(sys.argv)<4 else sys.argv[3], jsonindent=indent)
    else:
        print 'Usage: gen_data.py dictionary|phrase txt_filename [json_output_filename]'
        sys.exit(1)
        

