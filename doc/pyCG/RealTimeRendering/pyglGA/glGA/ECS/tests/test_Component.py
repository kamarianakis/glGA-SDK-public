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


class TestComponentA(unittest.TestCase):
    
    def test_init(self):
        """
        default constructor of Component class
        """
        print("\nTestComponentA:test_init() START")
        
        #myComponent = Component(100, "baseComponent", "abstract")
        myComponent = ComponentA()
        myComponent.name = "ComponentA"
        myComponent.type = "A"
        myComponent.id = 101
        
        self.assertEqual(myComponent.name, "ComponentA")
        self.assertEqual(myComponent.type,"A")
        self.assertEqual(myComponent.id, 101)
        print(f"myComponent class name is: {myComponent.get_classname()}")
        print("TestComponentA:test_init() END")  