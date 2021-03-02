"""
Test Scene Unit tests, part of the glGA SDK ECS
    
glGA SDK v2020.1 ECS (Entity Component System)
@Coopyright 2020-2021 George Papagiannakis

"""

import unittest
from Entity import Entity, EntityDfsIterator
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
        Sets up the ECSS both at ECSSManager level data structures
        as well as the underlying scenegraph
        
        mimicks the scenegraph created in TestCameraSystem setUp().
        
        hence we have two ways of setting up an ECSS: 
        a) High-level via the ECSSManager (recommended method)
        b) Low-level directly at scenegraph hierarchy level
        
        """
        self.WorldManager = ECSSManager()
        self.WorldManager2 = ECSSManager()
        
        """
        Rebuild the same scenegraph from test_System::TestCameraSystem class,
        via the ECSSManager:
        Scenegraph:
        
        root
            |                           |           |
            entityCam1,                 node4,      node3
            |-------|                    |           |----------|-----------|
            trans1, entityCam2           trans4     node5,      node6       trans3
            |       |                               |           |--------|
                    perspCam, trans2                trans5      node7    trans6
                                                                |
                                                                trans7
            
        """ 
        
        
        
    def test_init(self):
        """
        ECSSManager init components
        
        """
        
        print("TestECSSManager:test_init START".center(100, '-'))
        
        rootEntity = self.WorldManager.createEntity(Entity(name="RooT"))
        
        transUpdate = self.WorldManager.createSystem(TransformSystem("transUpdate", "TransformSystem", "001"))
        camUpdate = self.WorldManager.createSystem(CameraSystem("camUpdate", "CameraUpdate", "200"))
        dfsIterator = self.WorldManager.createIterator(rootEntity)
        
        
        
        for key, value in self.WorldManager._entities_components.items():
            print("\n entity: ",key, ":: with components: ", value)
        
        print(self.WorldManager._next_entity_id)
        self.assertEqual(id(self.WorldManager), id(self.WorldManager2))
        self.assertEqual(rootEntity, self.WorldManager._root)
        self.assertIsInstance(transUpdate, TransformSystem)
        self.assertIsInstance(camUpdate, CameraSystem)
        self.assertIsInstance(dfsIterator, EntityDfsIterator)
        
        
        print("TestECSSManager:test_init END".center(100, '-'))