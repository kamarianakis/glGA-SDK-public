"""
Test Entity Unit tests, part of the glGA SDK ECS
    
glGA SDK v2020.1 ECS (Entity Component System)
@Coopyright 2020-2021 George Papagiannakis

"""

import unittest
from Entity import *
from Component import *

class TestEntity(unittest.TestCase):
    
    @unittest.skip("Entity is ABC due to @abstractmethod update(), skipping the test")
    def test_parent(self):
        """ Entity test_parent() test
        
        """
        print("test_parent() test: START")
        entityA = Entity()
        entityB = Entity()
        entityB._parent = entityA
        self.assertEqual(entityA, entityB._parent)
        print("test_parent() test: END")
        
    @unittest.skip("Entity is ABC due to @abstractmethod update(), skipping the test")    
    def test_isEntity(self):
        """ Entity test_isEntity() test
        
        """
        print("test_isEntity() test: START")
        entityA = Entity()
        entityB = Entity()
        entityB._parent = entityA
        self.assertEqual(entityA.isEntity(), False)
        print("test_isEntity() test: END")

class TestEntityElement(unittest.TestCase):
    
    def test_init(self):
        """
        EntityElement init() test
        """
        print("TestEntityElement:test_init() START")
        gameObject = EntityElement() 
        gameObject2 = EntityElement(10)
        gameComponent = BasicTransform("Transform", "TRS", 200)
        
        gameObject2.addComponent(gameComponent)
        
        self.assertIsInstance(gameObject,EntityElement)
        self.assertIsInstance(gameObject._children, List)
        self.assertEqual(gameObject2._id,10)
        self.assertEqual(gameObject2.getComponent(0),gameComponent)
        
        gameObject2.removeComponent(gameComponent)
        self.assertEqual(gameObject2.getComponent(0), None)
        
        print(gameObject._children)
        print("TestEntityElement:test_init() END")

    def test_add(self):
        """
        EntityElement add() test
        """
        print("TestEntityElement:test_add() START")
        gameObject = EntityElement()
        gameObject2 = EntityElement()
        gameObject.add(gameObject2)
        self.assertIn(gameObject2,gameObject._children)
        self.assertEqual(gameObject._children[0], gameObject2)
        #print("gameObject._children[0]" + gameObject._children[0])
        print("TestEntityElement:test_add() END")
    
    
    def test_remove(self):
        """
        EntityElement remove() test
        """
        print("TestEntityElement:test_remove() START")
        gameObject = EntityElement()
        gameObject2 = EntityElement()
        gameObject.add(gameObject2)
        gameObject.remove(gameObject2)
        self.assertNotIn(gameObject2, gameObject._children)
        #print("gameObject._children[0]" + gameObject._children[0])
        print("TestEntityElement:test_remove() END")
    
    def test_getChild(self):
        """
        EntityElement test_getChild() test
        """
        print("TestEntityElement:test_getChild() START")
        gameObject = EntityElement()
        gameObject2 = EntityElement()
        gameObject.add(gameObject2)
        self.assertIn(gameObject2, gameObject._children)
        self.assertEqual(gameObject2, gameObject.getChild(0))
        #print("gameObject._children[0]" + gameObject._children[0])
        print("TestEntityElement:test_getChild() END")
        
    def test_getNumberOfChildren(self):
        """
        EntityElement test_getNumberOfChildren() test
        """
        print("TestEntityElement:test_getNumberOfChildren() START")
        gameObject = EntityElement(0)
        gameObject1 = EntityElement(1)
        gameObject2 = EntityElement(2)
        gameObject3 = EntityElement(3)
        gameObject.add(gameObject1)
        gameObject1.add(gameObject2)
        gameObject2.add(gameObject3)
        self.assertIn(gameObject1, gameObject._children)
        print(f"test_getNumberOfChildren() scene: \n {gameObject.update()}")
        self.assertEqual(gameObject.getNumberOfChildren(), 1)
        #print("gameObject._children[0]" + gameObject._children[0])
        print("TestEntityElement:test_getNumberOfChildren() END")
    
    def test_isEntity(self):
        """
        EntityElement isEntity() test
        """
        print("TestEntityElement:test_isEntity() START")
        gameObject = EntityElement()
        self.assertEqual(gameObject.isEntity(), True)
        
        print("TestEntityElement:test_isEntity() END")
        
    def test_update(self):
        """
        EntityElement update() test
        """
        print("TestEntityElement:test_update() START")
        gameObject = EntityElement("root")
        gameObject2 = EntityElement("node2")
        gameObject3 = EntityElement("node3")
        gameObject.add(gameObject2)
        gameObject2.add(gameObject3)
        
        self.assertIn(gameObject3, gameObject2._children)
        print(f"test_update() scene: \n {gameObject.update()}")
        print("TestEntityElement:test_update() END")

if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=3, exit=False)
        