"""
Test Scene Unit tests, part of the glGA SDK ECSS
    
glGA SDK v2021.0.5 ECSS (Entity Component System in a Scenegraph)
@Coopyright 2020-2021 George Papagiannakis

"""


import unittest

import numpy as np

import pyglGA.ECSS.utilities as util
from pyglGA.ECSS.Entity import Entity
from pyglGA.ECSS.Component import BasicTransform, Camera, RenderMesh
from pyglGA.ECSS.System import System, TransformSystem, CameraSystem, RenderSystem
from pyglGA.ext.Scene import Scene
from pyglGA.ECSS.ECSSManager import ECSSManager

from ext.Shader import InitGLShaderSystem, Shader, ShaderGLDecorator, RenderGLShaderSystem
from ext.VertexArray import VertexArray

class TestScene(unittest.TestCase):
    """Main body of Scene Unit Test class

    """
    def setUp(self):
        """
        Common setup for all unit tests
        
        Scenegraph for unit tests:
        
        root
            |---------------------------|           
            entityCam1,                 node4,      
            |-------|                    |--------------|----------|--------------|           
            trans1, entityCam2           trans4,        mesh4,     shaderDec4     vArray4
                    |                               
                    ortho, trans2                   
                                                                
                                                                
            
        """
        self.s1 = Scene()
        self.scene = Scene()    
        self.assertEqual(self.s1, self.scene)
        
        # Scenegraph with Entities, Components
        self.rootEntity = self.scene.world.createEntity(Entity(name="RooT"))
        self.entityCam1 = self.scene.world.createEntity(Entity(name="entityCam1"))
        self.scene.world.addEntityChild(self.rootEntity, self.entityCam1)
        self.trans1 = self.scene.world.addComponent(self.entityCam1, BasicTransform(name="trans1", trs=util.translate(1.0,2.0,3.0)))
        
        self.entityCam2 = self.scene.world.createEntity(Entity(name="entityCam2"))
        self.scene.world.addEntityChild(self.entityCam1, self.entityCam2)
        self.trans2 = self.scene.world.addComponent(self.entityCam2, BasicTransform(name="trans2", trs=util.translate(2.0,3.0,4.0)))
        self.orthoCam = self.scene.world.addComponent(self.entityCam2, Camera(util.ortho(-100.0, 100.0, -100.0, 100.0, 1.0, 100.0), "orthoCam","Camera","500"))
        
        self.node4 = self.scene.world.createEntity(Entity(name="node4"))
        self.scene.world.addEntityChild(self.rootEntity, self.node4)
        self.trans4 = self.scene.world.addComponent(self.node4, BasicTransform(name="trans4"))
        self.mesh4 = self.scene.world.addComponent(self.node4, RenderMesh(name="mesh4"))
        # a simple triangle
        self.vertexData = np.array([
            [0.0, 0.0, 0.0, 1.0],
            [0.5, 1.0, 0.0, 1.0],
            [1.0, 0.0, 0.0, 1.0]
        ],dtype=np.float,order='F') 
        # attached that simple triangle in a RenderMesh
        self.mesh4.vertex_attributes.append(self.vertexData)
        self.vArray4 = self.scene.world.addComponent(self.node4, VertexArray())
        
        # Systems
        self.transUpdate = self.scene.world.createSystem(TransformSystem("transUpdate", "TransformSystem", "001"))
        self.camUpdate = self.scene.world.createSystem(CameraSystem("camUpdate", "CameraUpdate", "200"))
        self.renderUpdate = self.scene.world.createSystem(RenderGLShaderSystem())
        self.initUpdate = self.scene.world.createSystem(InitGLShaderSystem())
        
        # decorated components and systems
        self.shaderDec4 = self.scene.world.addComponent(self.node4, ShaderGLDecorator(Shader()))

    def test_init(self):
        """
        default constructor of Component class
        """
        print("TestScene:test_init START".center(100, '-'))
        
        #check is scenegraph was initialised correctly by the world::ECSSManager
        self.assertEqual(id(self.scene), id(self.s1))
        self.assertEqual(self.rootEntity, self.scene.world.root)
        self.assertIsInstance(self.transUpdate, TransformSystem)
        self.assertIsInstance(self.camUpdate, CameraSystem)
        self.assertIsInstance(self.renderUpdate, RenderGLShaderSystem)
        self.assertIn(self.entityCam1, self.rootEntity._children)
        self.assertIn(self.node4, self.rootEntity._children)
        self.assertIn(self.trans4, self.node4._children)
        self.assertIn(self.mesh4, self.node4._children)
        self.assertIn(self.orthoCam, self.entityCam2._children)
        
        #self.scene.world.root.print()
        self.scene.world.print()
        
        # run test traversals one in the scene
        # root node is accessed via ECSSManagerObject.root property
        # normally these are run within the rendering loop
        #
        # 1. L2W traversal
        self.scene.world.traverse_visit(self.transUpdate, self.scene.world.root) 
        # 2. pre-camera Mr2c traversal
        self.scene.world.traverse_visit_pre_camera(self.camUpdate, self.orthoCam)
        # 3. run proper Ml2c traversal
        self.scene.world.traverse_visit(self.camUpdate, self.scene.world.root)
        # 4. run proper render traversal for once!
        self.scene.world.traverse_visit(self.renderUpdate, self.scene.world.root)
        
        # pre-pass scenegraph to initialise all GL context dependent geometry, shader classes
        #self.scene.world.traverse_visit(self.initUpdate, self.scene.world.root)
        
    
        print("TestScene:test_init END".center(100, '-'))
        
        
    def test_Shader_RenderShaderSystem_Decorators(self):
        """ test the decorated Shader and RenderSystem
        """
        print("TestScene:test_Shader_RenderShaderSystem_Decorators START".center(100, '-'))
        
        # create valid render context
        # need to do a scene pre-pass to init all Shader and VertexArrays after GL context is created
        # init in RenderMesh should copy all RenderMesh.vertex_attributes to VertexArray.attributes
        #
        # call a nice initSystem to call the init of all components and get over with it!
        
        
        print("TestScene:test_Shader_RenderShaderSystem_Decorators END".center(100, '-'))
    
    
    def test_render(self):
        """
        First time to test a RenderSystem in a Scene with Shader and VertexArray components
        """
        print("TestScene:test_render START".center(100, '-'))
        running = True
        # MAIN RENDERING LOOP
        self.scene.init(imgui=True, windowWidth = 1024, windowHeight = 768, windowTitle = "pyglGA ECSS Scene")
        
        # pre-pass scenegraph to initialise all GL context dependent geometry, shader classes
        # needs an active GL context
        self.scene.world.traverse_visit(self.initUpdate, self.scene.world.root)
        
        while running:
            running = self.scene.render(running)
            self.scene.world.traverse_visit(self.renderUpdate, self.scene.world.root)
        self.scene.shutdown()
        
        print("TestScene:test_render END".center(100, '-'))


if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=3, exit=False)