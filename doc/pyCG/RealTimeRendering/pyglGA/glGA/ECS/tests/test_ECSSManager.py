"""
Test Scene Unit tests, part of the glGA SDK ECS
    
glGA SDK v2020.1 ECS (Entity Component System)
@Coopyright 2020-2021 George Papagiannakis

"""

import unittest
from Entity import Entity
from Component import BasicTransform, Camera
from System import System, TransformSystem, CameraSystem, RenderSystem
from Scene import Scene
from ECSSManager import ECSSManager

class TestECSSManager(unittest.TestCase):
    """[summary]

    :param unittest: [description]
    :type unittest: [type]
    """
    
    def setUp(self):
        """
        
        """
        self.WorldManager = ECSSManager()
        self.WorldManager2 = ECSSManager()
        
        
        
    def test_init(self):
        """
        ECSSManager init components
        
        """
        
        self.WorldManager.createEntity(Entity(name="root"))
        
        for key in self.WorldManager._entities.keys():
            print("\n entity: ",key, ":: with components: ", self.WorldManager._entities[key])
        
        print(self.WorldManager._next_entity_id)
        self.assertEqual(id(self.WorldManager), id(self.WorldManager2))