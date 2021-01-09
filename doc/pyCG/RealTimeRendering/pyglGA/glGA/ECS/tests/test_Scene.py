"""
Test Scene Unit tests, part of the glGA SDK ECS
    
glGA SDK v2020.1 ECS (Entity Component System)
@Coopyright 2020-2021 George Papagiannakis

"""

import unittest
from Entity import *
from Component import *
from System import *
from Scene import *

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
        
        base = EntityElement(1)
        arm = EntityElement(2)
        forearm = EntityElement(3)
    
        base.add(arm)
        arm.add(forearm)
    
        scenegraph = base.update()
    
        print("Scenegraph is: ", scenegraph)
    
        print("TestScene:test_sampleScene() END")