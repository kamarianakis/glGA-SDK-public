"""
Test Component Unit tests, part of the glGA SDK ECS
    
glGA SDK v2020.1 ECS (Entity Component System)
@Coopyright 2020-2021 George Papagiannakis

"""
    
import unittest

from Component import *
from utilities import *
import numpy as np

class TestComponent(unittest.TestCase):
    
    @unittest.skip("Component is ABC due to @abstractmethod update(), skipping the test")
    def test_init(self):
        """
        default constructor of Component class
        """
        print("\nTestComponent:test_init() START")
        
        #myComponent = Component(100, "baseComponent", "abstract")
        myComponent = Component()
        myComponent.name = "baseComponent"
        myComponent.type = "abstract"
        myComponent.id = 100
        
        self.assertEqual(myComponent.name, "baseComponent")
        self.assertEqual(myComponent.type,"abstract")
        self.assertEqual(myComponent.id, 100)
        
        print("TestComponent:test_init() END")


class TestBasicTransform(unittest.TestCase):
    
    def test_init(self):
        """
        default constructor of Component class
        """
        print("\nTestComponentA:test_init() START")
        
        myComponent = BasicTransform()
        myComponent.name = "myComponent"
        myComponent.type = "BasicTransform"
        myComponent.id = 101
        myComponent.trs = translate(1.0, 2.0, 3.0)
        mT = np.array([
            [1.0,0.0,0.0,1.0],
            [0.0,1.0,0.0,2.0],
            [0.0,0.0,1.0,3.0],
            [0.0,0.0,0.0,1.0],
        ],dtype=np.float,order='F')
        
        self.assertEqual(myComponent.name, "myComponent")
        self.assertEqual(myComponent.type,"BasicTransform")
        self.assertEqual(myComponent.id, 101)
        np.testing.assert_array_equal(myComponent.trs,mT)
        
        print(f"Called {myComponent.name} update(): {myComponent.update()}")
        print("TestBasicTransform:test_init() END")  
        

class TestRenderMesh(unittest.TestCase):
    
    def test_init(self):
        """
        Default constructor for the basic RenderMesh class
        """        
        print("\TestRenderMesh:test_init() START")
        
        myComponent = RenderMesh()
        myComponent.name = "BasicMesh"
        myComponent.type = "B"
        myComponent.id = 201
        
        self.assertEqual(myComponent.name, "BasicMesh")
        self.assertEqual(myComponent.type,"B")
        self.assertEqual(myComponent.id, 201)
        print(f"Called {myComponent.name} update(): {myComponent.update()}")
        print("TestRenderMesh:test_init() END")  