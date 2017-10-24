
import unittest
import os

class Testone(unittest.TestCase):

    def setUp(self):
        os.system('touch /tmp/t1.log')


    def tearDown(self):
        os.system('rm /tmp/t1.log')

    def test1(self):
#        print 'hello i am test1'
        self.a1=range(10)
        self.a2=range(20)
        print self.a1
        self.assertEqual(self.a1,self.a2)


    def test2(self):
#        print 'hello i am test2'
        self.assertIsInstance(1,int)


if __name__ =='__main__':
    unittest.main()



