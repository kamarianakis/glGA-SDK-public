"""
Test class for Component from ECS
    
"""
    
import unittest
from Component import *


class TestComponent(unittest.TestCase):
    
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
        myComponent.name = "BasicTransform"
        myComponent.type = "A"
        myComponent.id = 101
        
        self.assertEqual(myComponent.name, "BasicTransform")
        self.assertEqual(myComponent.type,"A")
        self.assertEqual(myComponent.id, 101)
        print(f"Called {myComponent.name} update(): {myComponent.update()}")
        print("TestBasicTransform:test_init() END")  
        

class TestMesh(unittest.TestCase):
    
    def test_init(self):
        """
        Default constructor for the basic Mesh class
        """        
        print("\TestMesh:test_init() START")
        
        myComponent = Mesh()
        myComponent.name = "BasicMesh"
        myComponent.type = "B"
        myComponent.id = 201
        
        self.assertEqual(myComponent.name, "BasicMesh")
        self.assertEqual(myComponent.type,"B")
        self.assertEqual(myComponent.id, 201)
        print(f"Called {myComponent.name} update(): {myComponent.update()}")
        print("TestMesh:test_init() END")  