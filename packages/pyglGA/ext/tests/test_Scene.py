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
        """
        Common setup for all unit tests
        """
        self.s1 = Scene()
        self.s2 = Scene()    
        self.assertEqual(self.s1, self.s2)
    
    def test_init(self):
        """
        default constructor of Component class
        """
        print("TestScene:test_init START".center(100, '-'))
        
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
    
    
    def test_render(self):
        """
        
        """
        print("TestScene:test_render START".center(100, '-'))
        running = True
        # MAIN RENDERING LOOP
        self.s1.init(imgui=True, windowWidth = 1024, windowHeight = 768, windowTitle = "pyglGA ECSS Scene")
        
        while running:
            running = self.s1.render(running)
        self.s1.shutdown()
        
        print("TestScene:test_render END".center(100, '-'))


if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=3, exit=False)