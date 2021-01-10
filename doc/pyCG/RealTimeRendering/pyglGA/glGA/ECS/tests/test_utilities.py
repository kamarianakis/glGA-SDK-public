"""
Test utilities Unit tests, part of the glGA SDK ECS
    
glGA SDK v2020.1 ECS (Entity Component System)
@Coopyright 2020-2021 George Papagiannakis

"""

import unittest
import numpy as np

from utilities import *

class TestUtilities(unittest.TestCase):
    """ main class to test CG utilities and convenience functions """
    def test_vec(self):
        """
        test_vec function
        """
        print("\TestUtilities:test_vec() START")
        a = [1.0,0.0,0.0,1.0]
        vec_a = vec(a)  
        np_a = np.array([1.0,0.0,0.0,1.0],dtype=np.float,order='F')
        
        self.assertEqual(vec_a.tolist(), np_a.tolist())
        print(vec_a)
        print(np_a)
    
        print("TestUtilities:test_vec() END")
    
    def test_normalised(self):
        """
        test_normalised function
        """
        print("\TestUtilities:test_normalised() START")
        a = [2.0,2.0,0.0,1.0]
        vec_a = vec(a)  
        norm_vec = normalise(vec_a)
        norm_a = normalise(a) # in this case the simple list will be converted to numpy array first implicitly
        np_a = np.array([2.0,2.0,0.0,1.0],dtype=np.float,order='F')
        norm_np = np.array([0.666667,0.666667,0.0,0.333333],dtype=np.float,order='F')
        
        self.assertAlmostEqual(norm_vec.all(), norm_np.all())
        self.assertAlmostEqual(norm_a.all(), norm_np.all())
        print(norm_vec)
        print(norm_np)
        print(norm_a)
    
        print("TestUtilities:test_normalised() END")
    
    def test_lerp(self):
        """Test linear interpolation between two points"""
        print("\TestUtilities:test_lerp() START")
        
        # lerp between 0.0 to 1.0
        point0 = lerp(0.0, 1.0, 0.0)
        point1 = lerp(0.0, 1.0, 1.0)
        pointb = lerp(0.0, 1.0, 0.5)
        print(point0)
        print(point1)
        print(pointb)
        
        self.assertEqual(point0, 0)
        self.assertEqual(point1, 1)
        self.assertEqual(pointb, 0.5)
        
        print("\TestUtilities:test_lerp() END")
        
    def test_identity(self):
        """
        test_identity function
        """
        print("\TestUtilities:test_identity() START")
        matI = identity(4)
        np_i1 = np.ones((4,4))
        np_i4 = np.identity(4)
        np_i = np.array([
            [1.0,0.0,0.0,0.0],
            [0.0,1.0,0.0,0.0],
            [0.0,0.0,1.0,0.0],
            [0.0,0.0,0.0,1.0],
        ],dtype=np.float,order='F')
        
        self.assertEqual(matI.tolist(), np_i4.tolist())
        self.assertEqual(matI.tolist(), np_i.tolist())
        self.assertNotEqual(matI.tolist(), np_i1.tolist())
        print(matI)
        print(np_i)
        print(np_i1)
    
        print("TestUtilities:test_identity() END")
        
    def test_ortho(self):
        """
        test_ortho function, 
        tested against results from https://glm.g-truc.net/0.9.2/api/a00245.html
        """
        print("\TestUtilities:test_ortho() START")
        matOrtho = ortho(-100.0, 100.0, -100.0, 100.0, 1.0, 100.0)
        np_Ortho = np.array([
            [0.01,0.0,0.0,0.0],
            [0.0,0.01,0.0,0.0],
            [0.0,0.0,-0.020202,-1.0202],
            [0.0,0.0,0.0,1.0],
        ],dtype=np.float,order='F')
        
        self.assertAlmostEqual(matOrtho.all(), np_Ortho.all())
       
        print(matOrtho)
        print(np_Ortho)
    
        print("TestUtilities:test_ortho() END")
        
    def test_perspective(self):
        """
        test_perspective function, 
        tested against results from https://glm.g-truc.net/0.9.2/api/a00245.html
        """
        print("\TestUtilities:test_perspective() START")
        matPersp = perspective(90.0, 1, 0.1, 100)
        np_Persp = np.array([
            [0.61737,0.0,0.0,0.0],
            [0.0,0.61737,0.0,0.0],
            [0.0,0.0,-1.002,-0.2002],
            [0.0,0.0,-1.0,0.0],
        ],dtype=np.float,order='F')
        
        self.assertAlmostEqual(matPersp.all(), np_Persp.all())
       
        print(matPersp)
        print(np_Persp)
    
        print("TestUtilities:test_perspective() END")
        
    def test_frustum(self):
        """
        test_frustum function, 
        tested against results from https://glm.g-truc.net/0.9.2/api/a00245.html
        """
        print("\TestUtilities:test_frustum() START")
        matPersp = frustum(-10.0, 10.0,-10.0,10.0, 0.1, 100)
        np_Persp = np.array([
            [0.01,0.0,0.0,0.0],
            [0.0,0.01,0.0,0.0],
            [0.0,0.0,-1.002,-0.2002],
            [0.0,0.0,-1.0,0.0],
        ],dtype=np.float,order='F')
        
        self.assertAlmostEqual(matPersp.all(), np_Persp.all())
       
        print(matPersp)
        print(np_Persp)
    
        print("TestUtilities:test_frustum() END")