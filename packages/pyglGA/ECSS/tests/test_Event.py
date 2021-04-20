"""
Test Event Unit tests, part of the glGA SDK ECSS
    
glGA SDK v2021.0.5 ECSS (Entity Component System in a Scenegraph)
@Coopyright 2020-2021 George Papagiannakis

"""


import unittest
import time
import numpy as np

import pyglGA.ECSS.utilities as util
from pyglGA.ECSS.System import System, TransformSystem, CameraSystem
from pyglGA.ECSS.Entity import Entity
from pyglGA.ECSS.Component import BasicTransform, Camera
from pyglGA.ECSS.Event import Event

class TestEvent(unittest.TestCase):
    
    def test_init(self):
        """simple tests for Event dataclass
        """
        trsMat = util.translate(10.0,20.0,30.0)
        e = Event("OnUpdate", 100, trsMat)
        
        mT = np.array([
            [1.0,0.0,0.0,10.0],
            [0.0,1.0,0.0,20.0],
            [0.0,0.0,1.0,30.0],
            [0.0,0.0,0.0,1.0],
        ],dtype=np.float,order='F')
        
        self.assertEqual(mT.tolist(), e.value.tolist())
        self.assertEqual(e.name, "OnUpdate")
        self.assertEqual(e.id, 100)
        np.testing.assert_array_equal(e.value,mT)
        
        e.id = 101
        self.assertEqual(e.id, 101)
        
        print(e.value)
        print("\n Event e: ",e)