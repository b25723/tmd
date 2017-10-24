import unittest

class demo(unittest.TestCase):
    def setUp(self):
        print ''
        print 'create env'

    def tearDown(self):
        print 'clean env'
        print ''

    def test_upper(self):
        self.assertEqual('foo'.upper(),'FOO')

    @unittest.skip("I don't want to run this case.")
    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s='hello world'
        self.assertEqual(s.split(),['hello','world'])

    @classmethod
    def setUpClass(cls):
        print 'start only execute once'

    @classmethod
    def tearDownClass(cls):
        print 'stop only execute once'

if __name__ == '__main__':
    #unittest.main()
    suite=unittest.TestSuite()
    tests=[demo('test_upper'),demo('test_split'),demo('test_isupper')]
    suite.addTests(tests)
    runner=unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
