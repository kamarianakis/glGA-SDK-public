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
        
    
class TestTransformUpdate(unittest.TestCase):
    def test_TransformUpdate_use(self):
        """
        Entity EntityDfsIterator() test
        """
        print("TestTransformUpdate:test_TransformUpdate_use() START")
        gameObject = Entity("root", "Group", "1")
        gameObject2 = Entity("node2", "Group", "2")
        gameObject3 = Entity("node3", "Group", "3")
        gameObject4 = Entity("node4", "Group", "4")
        gameObject5 = Entity("node5", "Group", "5")
        gameObject6 = Entity("node6", "Group", "6")
        gameObject7 = Entity("node7", "Group", "7")
        trans4 = BasicTransform("trans4", "Transform", "7")
        trans5 = BasicTransform("trans5", "Transform", "8")
        trans6 = BasicTransform("trans6", "Transform", "9")
        gameObject.add(gameObject2)
        gameObject.add(gameObject4)
        gameObject.add(gameObject7)
        gameObject2.add(gameObject3)
        gameObject2.add(gameObject5)
        gameObject3.add(gameObject6)
        gameObject4.add(trans4)
        gameObject5.add(trans5)
        gameObject6.add(trans6)
        
        self.assertIn(gameObject2, gameObject._children)
        self.assertIn(gameObject4, gameObject._children)
        self.assertIn(trans4, gameObject4._children)
        self.assertIn(gameObject3, gameObject2._children)
        self.assertIn(trans5, gameObject5._children)
        
        #test the EntityDfsIterator to traverse the above ECS scenegraph
        dfsIterator = iter(gameObject)
        print(gameObject)
        
        #instantiate a new TransformUpdate System to visit all scenegraph componets
        transUpdate = TransformUpdate("transUpdate", "TransformUpdate", "001")
        
        nodePath = []
        done_traversing = False
        while(not done_traversing):
            try:
                traversedComp = next(dfsIterator)
            except StopIteration:
                print("\n-------- end of Scene reached, traversed all Components!")
                done_traversing = True
            else:
                if (traversedComp is not None): #only if we reached end of Entity's children traversedComp is None
                    print(traversedComp)
                    
                    #accept a TransformUpdate visitor System for each Component that can accept it (BasicTransform)
                    traversedComp.accept(transUpdate) #calls specific concrete Visitor's apply(), which calls specific concrete Component's update
                
                    nodePath.append(traversedComp)
        
        #print("".join(str(nodePath)))
        
        
        
        print("TestTransformUpdate:test_TransformUpdate_use() END")
        

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
        
        print("TestSystem:test_update() END")
        

if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=3, exit=False)