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

    