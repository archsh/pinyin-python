# -*- coding:utf-8 -*-

import sys
sys.path.append('../')
import datetime
import pinyin
import unittest


class DefaultTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_version(self):
        self.assertIsNotNone(pinyin.__version__, '0.1')
    
    def test_loading(self):
        py = pinyin.Pinyin()
        self.assertGreater(len(py._pydata),20000)
    
    def test_query(self):
        t1 = datetime.datetime.now()
        py = pinyin.Pinyin()
        t2 = datetime.datetime.now()
        ret = py.query('d')
        t3 = datetime.datetime.now()
        #print ret
        print 't2-t1:',t2-t1
        print 't3-t2:',t3-t2
        #for w in py.query('ti'): print w
        #for w in py.query('bei'): print w
        #for w in py.query('da'): print w
        #for w in py.query('ch'): print w
    
        
    


def suite():
    suite = unittest.TestSuite()
    suite.addTest(DefaultTestCase('test_version'))
    suite.addTest(DefaultTestCase('test_loading'))
    suite.addTest(DefaultTestCase('test_query'))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite', verbosity=2)
