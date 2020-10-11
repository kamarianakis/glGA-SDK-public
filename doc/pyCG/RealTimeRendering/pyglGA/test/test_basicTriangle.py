import unittest
from basicTriangle import *

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
        
class TestinitTriangle(unittest.TestCase):
        
    def test_InitTriangle_returns(self):
        """
        tests the return values of initTriangle()
        """
        #instance_under_test = ClassThatContainsMethod() 
        # #so that we can access its methods later ClassThatContainsMethod.method() in test asserts
        
        tShader, tVAO, tVBO = initTriangle()
        self.assertIsNotNone(tShader)
        self.assertIsNotNone(tVAO)
        self.assertIsNotNone(tVBO)

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=3, exit=False )