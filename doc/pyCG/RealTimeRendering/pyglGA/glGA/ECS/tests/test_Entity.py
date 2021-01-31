"""
Test EntityI Unit tests, part of the glGA SDK ECS
    
glGA SDK v2020.1 ECS (EntityI Component System)
@Coopyright 2020-2021 George Papagiannakis

"""

import unittest
from Entity import *
from Component import *



class TestEntity(unittest.TestCase):
    
    def test_init(self):
        """
        Entity init() test
        """
        print("TestEntity:test_init() START")
        gameObject = Entity() 
        gameObject2 = Entity("gameObject2", "Group", 10)
        gameComponent = BasicTransform("Transform", "TRS", 200)
        
        gameObject2.add(gameComponent)
        
        self.assertIsInstance(gameObject,Entity)
        self.assertIsInstance(gameObject._children, List)
        self.assertEqual(gameObject2._id,10)
        self.assertEqual(gameObject2.getChild(0),gameComponent)
        
        gameObject2.remove(gameComponent)
        self.assertEqual(gameObject2.getChild(0), None)
        
        print(gameObject._children)
        print("TestEntity:test_init() END")

    def test_add(self):
        """
        Entity add() test
        """
        print("TestEntity:test_add() START")
        gameObject = Entity()
        gameObject2 = Entity()
        gameObject.add(gameObject2)
        self.assertIn(gameObject2,gameObject._children)
        self.assertEqual(gameObject._children[0], gameObject2)
        #print("gameObject._children[0]" + gameObject._children[0])
        print("TestEntity:test_add() END")
    
    
    def test_remove(self):
        """
        Entity remove() test
        """
        print("TestEntity:test_remove() START")
        gameObject = Entity()
        gameObject2 = Entity()
        gameObject.add(gameObject2)
        gameObject.remove(gameObject2)
        self.assertNotIn(gameObject2, gameObject._children)
        #print("gameObject._children[0]" + gameObject._children[0])
        print("TestEntity:test_remove() END")
    
    def test_getChild(self):
        """
        Entity test_getChild() test
        """
        print("TestEntity:test_getChild() START")
        gameObject = Entity()
        gameObject2 = Entity()
        gameObject.add(gameObject2)
        self.assertIn(gameObject2, gameObject._children)
        self.assertEqual(gameObject2, gameObject.getChild(0))
        #print("gameObject._children[0]" + gameObject._children[0])
        print("TestEntity:test_getChild() END")
        
    def test_getNumberOfChildren(self):
        """
        Entity test_getNumberOfChildren() test
        """
        print("TestEntity:test_getNumberOfChildren() START")
        gameObject = Entity(0)
        gameObject1 = Entity(1)
        gameObject2 = Entity(2)
        gameObject3 = Entity(3)
        gameObject.add(gameObject1)
        gameObject1.add(gameObject2)
        gameObject2.add(gameObject3)
        self.assertIn(gameObject1, gameObject._children)
        print(f"test_getNumberOfChildren() scene: \n {gameObject.update()}")
        self.assertEqual(gameObject.getNumberOfChildren(), 1)
        #print("gameObject._children[0]" + gameObject._children[0])
        print("TestEntity:test_getNumberOfChildren() END")
    
    def test_isEntity(self):
        """
        Entity isEntity() test
        """
        print("TestEntity:test_isEntity() START")
        gameObject = Entity()
        self.assertEqual(gameObject.isEntity(), True)
        
        print("TestEntity:test_isEntity() END")
        
    def test_print(self):
        """
        Entity print() test
        """
        print("TestEntity:test_print() START")
        gameObject = Entity("root", "Group", "1")
        gameObject2 = Entity("node2", "Group", "2")
        gameObject3 = Entity("node3", "Group", "3")
        gameObject4 = Entity("node4", "Group", "4")
        gameObject5 = Entity("node5", "Group", "5")
        gameObject6 = Entity("node6", "Group", "6")
        trans4 = BasicTransform("trans4", "Transform", "1")
        trans5 = BasicTransform("trans5", "Transform", "2")
        trans6 = BasicTransform("trans6", "Transform", "3")
        gameObject.add(gameObject2)
        gameObject2.add(gameObject3)
        gameObject.add(gameObject4)
        gameObject2.add(gameObject5)
        gameObject3.add(gameObject6)
        gameObject4.add(trans4)
        gameObject5.add(trans5)
        gameObject6.add(trans6)
        
        self.assertIn(gameObject3, gameObject2._children)
        print(f"\nscenegraph is: {gameObject.print()}")
        print("TestEntity:test_print() END")
        
    

if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=3, exit=False)
        