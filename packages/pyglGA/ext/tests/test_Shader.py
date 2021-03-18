"""
Test Shader Unit tests, part of the glGA SDK ECSS
    
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

from pyglGA.ext.Shader import Shader

class TestShader(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_init(self):
        pass
    
    def test_update(self):
        pass
        

if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=3, exit=False)