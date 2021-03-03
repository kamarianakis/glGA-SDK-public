"""
Test Scene Unit tests, part of the glGA SDK ECS
    
glGA SDK v2020.1 ECS (Entity Component System)
@Coopyright 2020-2021 George Papagiannakis

"""

import unittest
import utilities as util
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
        # Scenegraph with Entities, Components
        self.rootEntity = self.WorldManager.createEntity(Entity(name="RooT"))
        self.entityCam1 = self.WorldManager.createEntity(Entity(name="entityCam1"))
        self.WorldManager.addEntityChild(self.rootEntity, self.entityCam1)
        self.trans1 = self.WorldManager.addComponent(self.entityCam1, BasicTransform(name="trans1", trs=util.translate(1.0,2.0,3.0)))
        
        self.entityCam2 = self.WorldManager.createEntity(Entity(name="entityCam2"))
        self.WorldManager.addEntityChild(self.entityCam1, self.entityCam2)
        self.trans2 = self.WorldManager.addComponent(self.entityCam2, BasicTransform(name="trans2", trs=util.translate(2.0,3.0,4.0)))
        self.perspCam = self.WorldManager.addComponent(self.entityCam2, Camera(util.ortho(-100.0, 100.0, -100.0, 100.0, 1.0, 100.0), "perspCam","Camera","500"))
        
        self.node4 = self.WorldManager.createEntity(Entity(name="node4"))
        self.WorldManager.addEntityChild(self.rootEntity, self.node4)
        self.trans4 = self.WorldManager.addComponent(self.node4, BasicTransform(name="trans4"))
        
        self.node3 = self.WorldManager.createEntity(Entity(name="node3"))
        self.WorldManager.addEntityChild(self.rootEntity, self.node3)
        self.trans3 = self.WorldManager.addComponent(self.node3, BasicTransform(name="trans3", trs=util.translate(3.0,3.0,3.0)))
        
        self.node5 = self.WorldManager.createEntity(Entity(name="node5"))
        self.WorldManager.addEntityChild(self.node3, self.node5)
        self.trans5 = self.WorldManager.addComponent(self.node5, BasicTransform(name="trans5"))
        
        self.node6 = self.WorldManager.createEntity(Entity(name="node6"))
        self.WorldManager.addEntityChild(self.node3, self.node6)
        self.trans6 = self.WorldManager.addComponent(self.node6, BasicTransform(name="trans6", trs=util.translate(6.0,6.0,6.0)))
        
        self.node7 = self.WorldManager.createEntity(Entity(name="node7"))
        self.WorldManager.addEntityChild(self.node6, self.node7)
        self.trans7 = self.WorldManager.addComponent(self.node7, BasicTransform(name="trans7", trs=util.translate(7.0,7.0,7.0)))
        
        # Systems
        self.transUpdate = self.WorldManager.createSystem(TransformSystem("transUpdate", "TransformSystem", "001"))
        self.camUpdate = self.WorldManager.createSystem(CameraSystem("camUpdate", "CameraUpdate", "200"))
        
        # Iterators
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
        
        self.assertIn(self.entityCam1, self.rootEntity._children)
        self.assertIn(self.node4, self.rootEntity._children)
        self.assertIn(self.trans4, self.node4._children)
        self.assertIn(self.node3, self.rootEntity._children)
        self.assertIn(self.trans5, self.node5._children)
        self.assertIn(self.trans7, self.node7._children)
        self.assertIn(self.perspCam, self.entityCam2._children)
        
        
        print("TestECSSManager:test_init END".center(100, '-'))
    
    
    def test_addComponent(self):
        """
        ECSSManager addComponent
        """
        
        print("TestECSSManager:test_addComponent START".center(100, '-'))
        
        compTrans = self.entityCam1.getChildByType(BasicTransform.getClassName())
        
        self.assertEqual(self.rootEntity, self.entityCam1.parent)
        self.assertEqual(compTrans.parent, self.entityCam1)
        self.assertEqual(self.trans1.parent, self.entityCam1)
        self.assertEqual(compTrans, self.trans1)
        self.assertIsInstance(self.trans1, BasicTransform)
        
        
        
        print("TestECSSManager:test_addComponent END".center(100, '-'))