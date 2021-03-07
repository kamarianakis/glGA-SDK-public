"""
Test Scene Unit tests, part of the glGA SDK ECSS
    
glGA SDK v2021.0.5 ECSS (Entity Component System in a Scenegraph)
@Coopyright 2020-2021 George Papagiannakis

"""

import unittest
from Entity import Entity
from Component import BasicTransform, Camera
from System import System, TransformSystem, CameraSystem, RenderSystem
from Scene import Scene

class TestScene(unittest.TestCase):
    """Main body of Scene Unit Test class

    :param unittest: [description]
    :type unittest: [type]
    """
    def test_new(self):
        """
        default constructor of Component class
        """
        print("\TestScene:test_new() START")
        s1 = Scene()
        s2 = Scene()    
        self.assertEqual(s1, s2)
    
        print("TestScene:test_new() END")
        
    def test_sampleScene(self):
        """
        default constructor of Component class
        """
        print("\TestScene:test_sampleScene() START")
        
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
    
        print("TestScene:test_sampleScene() END")


if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=3, exit=False)