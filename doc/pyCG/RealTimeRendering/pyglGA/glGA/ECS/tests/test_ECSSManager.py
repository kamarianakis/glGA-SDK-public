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
        
        """
        print(self.WorldManager._next_entity_id)
        self.assertEqual(id(self.WorldManager), id(self.WorldManager2))