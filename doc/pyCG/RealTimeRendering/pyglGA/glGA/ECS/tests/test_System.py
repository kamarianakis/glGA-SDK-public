"""
Test System Unit tests, part of the glGA SDK ECS
    
glGA SDK v2020.1 ECS (Entity Component System)
@Coopyright 2020-2021 George Papagiannakis

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
        mySystem = RenderGPU()
        mySystem.name = "RenderGPU"
        mySystem.type = "System"
        mySystem.id = 101
        
        self.assertEqual(mySystem.name, "RenderGPU")
        self.assertEqual(mySystem.type,"System")
        self.assertEqual(mySystem.id, 101)
        
        print("TestRenderGPU:test_init() END")
    
    def test_update(self):
        """
        test_update of System Depth First Search traversal
        based on https://likegeeks.com/depth-first-search-in-python/
        """
        print("\TestSystem:test_update() START")
        
        #mySystem = System(100, "baseSystem", "abstract")
        mySystem = RenderGPU()
        mySystem.name = "mySystem"
        mySystem.type = "Rendering"
        mySystem.id = 102
        
        self.assertEqual(mySystem.name, "mySystem")
        self.assertEqual(mySystem.type,"Rendering")
        self.assertEqual(mySystem.id, 102)
        
        #create a sample graph to test the system
        graph = {"A":["D", "C", "B"],
                "B":["E"],
                "C":["G", "F"],
                "D":["H"],
                "E":["I"],
                "F":["J"]}
        
        
        print("\n\n DFS PATH non recursive-------------------")
        DFS_path = mySystem.update(False, graph, "A")
        print(DFS_path)
        
        print("\n\n DFS PATH recursive-------------------")
        DFS_path_r = mySystem.update(True, graph, "A")
        print(" ".join(DFS_path_r))
        
        print("TestSystem:test_update() END")