import unittest
from basicCubeGUI import *
# to run, execute "python -m unittest" in the folder above the 'test' folder where the source py modules are

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
        
class TestinitCube(unittest.TestCase):
        
    def test_InitCube_returns(self):
        """
        tests the return values of initCube()
        """
        #instance_under_test = ClassThatContainsMethod() 
        # #so that we can access its methods later ClassThatContainsMethod.method() in test asserts
        
        tShader, tVAO, tVBO = initCube()
        self.assertIsNotNone(tShader)
        self.assertIsNotNone(tVAO)
        self.assertIsNotNone(tVBO)

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=3, exit=False )