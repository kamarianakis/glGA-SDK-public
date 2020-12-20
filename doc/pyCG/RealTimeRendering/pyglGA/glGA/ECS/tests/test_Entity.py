import unittest
from Entity import *


class TestEntity(unittest.TestCase):
    
    @unittest.skip("Entity is ABC due to @abstractmethod update()")
    def test_parent(self):
        """ Entity test_parent() test
        
        """
        print("test_parent() test: START")
        entityA = Entity()
        entityB = Entity()
        entityB._parent = entityA
        self.assertEqual(entityA, entityB._parent)
        print("test_parent() test: END")
        
    @unittest.skip("Entity is ABC due to @abstractmethod update()")    
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
        print("test_init: START")
        gameObject = SceneEntity() 
        
        self.assertIsInstance(gameObject,SceneEntity)
        
        print("test_init: END")

if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=3, exit=False)
        