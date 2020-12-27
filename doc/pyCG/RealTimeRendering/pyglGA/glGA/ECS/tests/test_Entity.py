import unittest
from Entity import *


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

class TestEntityNode(unittest.TestCase):
    
    def test_init(self):
        """
        EntityNode init() test
        """
        print("TestEntityNode:test_init() START")
        gameObject = EntityNode() 
        
        self.assertIsInstance(gameObject,EntityNode)
        self.assertIsInstance(gameObject._children, List)
        
        print(gameObject._children)
        print("TestEntityNode:test_init() END")

    def test_add(self):
        """
        EntityNode add() test
        """
        print("TestEntityNode:test_add() START")
        gameObject = EntityNode()
        gameObject2 = EntityNode()
        gameObject.add(gameObject2)
        self.assertIn(gameObject2,gameObject._children)
        self.assertEqual(gameObject._children[0], gameObject2)
        #print("gameObject._children[0]" + gameObject._children[0])
        print("TestEntityNode:test_add() END")
    
    
    def test_remove(self):
        """
        EntityNode remove() test
        """
        print("TestEntityNode:test_remove() START")
        gameObject = EntityNode()
        gameObject2 = EntityNode()
        gameObject.add(gameObject2)
        gameObject.remove(gameObject2)
        self.assertNotIn(gameObject2, gameObject._children)
        #print("gameObject._children[0]" + gameObject._children[0])
        print("TestEntityNode:test_remove() END")
    
    def test_getChild(self):
        """
        EntityNode test_getChild() test
        """
        print("TestEntityNode:test_getChild() START")
        gameObject = EntityNode()
        gameObject2 = EntityNode()
        gameObject.add(gameObject2)
        self.assertIn(gameObject2, gameObject._children)
        self.assertEqual(gameObject2, gameObject.getChild(0))
        #print("gameObject._children[0]" + gameObject._children[0])
        print("TestEntityNode:test_getChild() END")
        
    def test_getNumberOfChildren(self):
        """
        EntityNode test_getNumberOfChildren() test
        """
        print("TestEntityNode:test_getNumberOfChildren() START")
        gameObject = EntityNode(0)
        gameObject1 = EntityNode(1)
        gameObject2 = EntityNode(2)
        gameObject3 = EntityNode(3)
        gameObject.add(gameObject1)
        gameObject1.add(gameObject2)
        gameObject2.add(gameObject3)
        self.assertIn(gameObject1, gameObject._children)
        print(f"test_getNumberOfChildren() scene: \n {gameObject.update()}")
        self.assertEqual(gameObject.getNumberOfChildren(), 1)
        #print("gameObject._children[0]" + gameObject._children[0])
        print("TestEntityNode:test_getNumberOfChildren() END")
    
    def test_isEntity(self):
        """
        EntityNode isEntity() test
        """
        print("TestEntityNode:test_isEntity() START")
        gameObject = EntityNode()
        self.assertEqual(gameObject.isEntity(), True)
        
        print("TestEntityNode:test_isEntity() END")
        
    def test_update(self):
        """
        EntityNode update() test
        """
        print("TestEntityNode:test_update() START")
        gameObject = EntityNode("root")
        gameObject2 = EntityNode("node2")
        gameObject3 = EntityNode("node3")
        gameObject.add(gameObject2)
        gameObject2.add(gameObject3)
        
        self.assertIn(gameObject3, gameObject2._children)
        print(f"test_update() scene: \n {gameObject.update()}")
        print("TestEntityNode:test_update() END")

if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=3, exit=False)
        