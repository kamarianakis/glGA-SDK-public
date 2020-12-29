"""
Test System from ECS
    
"""


import unittest
from System import *


class TestSystem(unittest.TestCase):
    def test_init(self):
        """
        default constructor of System class
        """
        print("\TestSystem:test_init() START")
        
        #mySystem = System(100, "baseSystem", "abstract")
        mySystem = System()
        mySystem.name = "baseSystem"
        mySystem.type = "abstract"
        mySystem.id = 100
        
        self.assertEqual(mySystem.name, "baseSystem")
        self.assertEqual(mySystem.type,"abstract")
        self.assertEqual(mySystem.id, 100)
        
        print("TestSystem:test_init() END")
        

class TestRenderGPU(unittest.TestCase):
    def test_init(self):
        """
        default constructor of System class
        """
        print("\TestRenderGPU:test_init() START")
        
        #mySystem = System(100, "baseSystem", "abstract")
        mySystem = System()
        mySystem.name = "RenderGPU"
        mySystem.type = "System"
        mySystem.id = 101
        
        self.assertEqual(mySystem.name, "RenderGPU")
        self.assertEqual(mySystem.type,"System")
        self.assertEqual(mySystem.id, 101)
        
        print("TestRenderGPU:test_init() END")