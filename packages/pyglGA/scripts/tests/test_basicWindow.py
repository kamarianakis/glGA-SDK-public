import unittest
from basicWindow import init

class Testinit(unittest.TestCase):
        
    def test_Init_returns(self):
        """
        tests the return values of init()
        """
        #instance_under_test = ClassThatContainsMethod() 
        # #so that we can access its methods later ClassThatContainsMethod.method() in test asserts
        
        tWin, tContext, tVersion = init()
        self.assertIsNotNone(tWin)
        self.assertIsNotNone(tContext)
        self.assertIsNotNone(tVersion)

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=3, exit=False )