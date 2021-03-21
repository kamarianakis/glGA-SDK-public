"""
Test VertexArray Unit tests, part of the glGA SDK ECSS
    
glGA SDK v2021.0.5 ECSS (Entity Component System in a Scenegraph)
@Coopyright 2020-2021 George Papagiannakis

"""

import unittest

import pyglGA.ECSS.utilities as util
from pyglGA.ECSS.Entity import Entity
from pyglGA.ECSS.Component import BasicTransform, Camera, RenderMesh
from pyglGA.ECSS.System import System, TransformSystem, CameraSystem, RenderSystem
from pyglGA.ext.Scene import Scene
from pyglGA.ECSS.ECSSManager import ECSSManager

from pyglGA.ext.VertexArray import VertexArray


@unittest.skip("Requires active GL context, skipping the test")
class TestVertexArray(unittest.TestCase):
    
    def setUp(self):
        print("TestVertexArray:setUp START".center(100, '-'))
        
        self.myVertexArray = VertexArray()
        
        print("TestVertexArray:setUp END".center(100, '-'))
    
    def test_init(self):
        print("TestVertexArray:test_init START".center(100, '-'))
        
        self.assertEqual(self.myVertexArray.name, "VertexArray")
        self.assertEqual(self.myVertexArray.type,"VertexArray")
        
        print("TestVertexArray:test_init END".center(100, '-'))
    
    
    def test_update(self):
        print("TestVertexArray:test_update START".center(100, '-'))
        
        
        
        print("TestVertexArray:test_update END".center(100, '-'))
        

if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=3, exit=False)