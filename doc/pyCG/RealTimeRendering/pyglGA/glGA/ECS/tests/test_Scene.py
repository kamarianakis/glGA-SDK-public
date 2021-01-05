"""
Test Scene Unit tests, part of the glGA SDK ECS
    
glGA SDK v2020.1 ECS (Entity Component System)
@Coopyright 2020-2021 George Papagiannakis

"""

import unittest
from Entity import *
from Component import *
from System import *

class TestScene(unittest.TestCase):
    """Main body of Scene Unit Test class

    :param unittest: [description]
    :type unittest: [type]
    """
    def test_init(self):
        """
        default constructor of Component class
        """
        print("\TestScene:test_init() START")
        
        
        
        print("TestScene:test_init() END")