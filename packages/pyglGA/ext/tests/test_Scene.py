"""
Test Scene Unit tests, part of the glGA SDK ECSS
    
glGA SDK v2021.0.5 ECSS (Entity Component System in a Scenegraph)
@Coopyright 2020-2021 George Papagiannakis

"""

import unittest
from pyglGA.ECSS.Entity import Entity
from pyglGA.ECSS.Component import BasicTransform, Camera
from pyglGA.ECSS.System import System, TransformSystem, CameraSystem, RenderSystem
from pyglGA.ext.Scene import Scene

class TestScene(unittest.TestCase):
    """Main body of Scene Unit Test class

    """
    def setUp(self):
        pass
    
    def test_init(self):
        """
        default constructor of Component class
        """
        print("TestScene:test_init START".center(100, '-'))
        s1 = Scene()
        s2 = Scene()    
        self.assertEqual(s1, s2)
        
        base = Entity("base", "group", 1)
        arm = Entity("arm", "group",2)
        forearm = Entity("forearm", "group",3)
    
        baseShape = Entity("baseShape", "shape",4)
        armShape = Entity("armShape", "shape", 5)
        forearmShape = Entity("forearmShape", "shape", 6)
    
        base.add(arm)
        base.add(baseShape)
        arm.add(forearm)
        arm.add(armShape)
        forearm.add(forearmShape)
    
        scenegraph = base.update()
    
        print("Scenegraph is: ", scenegraph)
    
        print("TestScene:test_init END".center(100, '-'))
        

if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=3, exit=False)