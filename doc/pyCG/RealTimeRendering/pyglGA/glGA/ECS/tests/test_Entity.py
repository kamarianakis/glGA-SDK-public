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

class TestSceneEntity(unittest.TestCase):
    
    def test_init(self):
        """
        SceneEntity init() test
        """
        print("TestSceneEntity:test_init() START")
        gameObject = SceneEntity() 
        
        self.assertIsInstance(gameObject,SceneEntity)
        self.assertIsInstance(gameObject._children, List)
        
        print(gameObject._children)
        print("TestSceneEntity:test_init() END")

    def test_add(self):
        """
        SceneEntity add() test
        """
        print("TestSceneEntity:test_add() START")
        gameObject = SceneEntity()
        gameObject2 = SceneEntity()
        gameObject.add(gameObject2)
        self.assertIn(gameObject2,gameObject._children)
        self.assertEqual(gameObject._children[0], gameObject2)
        #print("gameObject._children[0]" + gameObject._children[0])
        print("TestSceneEntity:test_add() END")
    
    
    def test_remove(self):
        """
        SceneEntity remove() test
        """
        print("TestSceneEntity:test_remove() START")
        gameObject = SceneEntity()
        gameObject2 = SceneEntity()
        gameObject.add(gameObject2)
        gameObject.remove(gameObject2)
        self.assertNotIn(gameObject2, gameObject._children)
        #print("gameObject._children[0]" + gameObject._children[0])
        print("TestSceneEntity:test_remove() END")
        
    def test_isEntity(self):
        """
        SceneEntity isEntity() test
        """
        print("TestSceneEntity:test_isEntity() START")
        gameObject = SceneEntity()
        self.assertEqual(gameObject.isEntity(), True)
        
        print("TestSceneEntity:test_isEntity() END")
        
    def test_update(self):
        """
        SceneEntity update() test
        """
        print("TestSceneEntity:test_update() START")
        gameObject = SceneEntity("root")
        gameObject2 = SceneEntity("node2")
        gameObject3 = SceneEntity("node3")
        gameObject.add(gameObject2)
        gameObject2.add(gameObject3)
        
        self.assertIn(gameObject3, gameObject2._children)
        print(f"test_update() scene: \n {gameObject.update()}")
        print("TestSceneEntity:test_update() END")

if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=3, exit=False)
        