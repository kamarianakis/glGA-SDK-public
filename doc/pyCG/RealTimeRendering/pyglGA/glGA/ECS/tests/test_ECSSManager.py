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
        self.rootEntity = self.WorldManager.createEntity(Entity(name="RooT"))
        self.entityCam1 = self.WorldManager.createEntity(Entity(name="entityCam1"))
        
        self.transUpdate = self.WorldManager.createSystem(TransformSystem("transUpdate", "TransformSystem", "001"))
        self.camUpdate = self.WorldManager.createSystem(CameraSystem("camUpdate", "CameraUpdate", "200"))
        self.dfsIterator = self.WorldManager.createIterator(self.rootEntity)
        
        
    def test_init(self):
        """
        ECSSManager init components
        
        """
        
        print("TestECSSManager:test_init START".center(100, '-'))
        
        
        for key, value in self.WorldManager._entities_components.items():
            print("\n entity: ",key, ":: with components: ", value)
        
        print(self.WorldManager._next_entity_id)
        self.assertEqual(id(self.WorldManager), id(self.WorldManager2))
        self.assertEqual(self.rootEntity, self.WorldManager._root)
        self.assertIsInstance(self.transUpdate, TransformSystem)
        self.assertIsInstance(self.camUpdate, CameraSystem)
        self.assertIsInstance(self.dfsIterator, EntityDfsIterator)
        
        
        print("TestECSSManager:test_init END".center(100, '-'))
    
    
    def test_addComponent(self):
        """
        ECSSManager addComponent
        """
        
        print("TestECSSManager:test_addComponent START".center(100, '-'))
        
        self.WorldManager.addComponent(self.entityCam1, BasicTransform(name="trans1"))
        
        
        
        print("TestECSSManager:test_addComponent END".center(100, '-'))