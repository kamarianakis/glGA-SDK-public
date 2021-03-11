"""
Test Viewer classes, part of the pyglGA SDK ECSS
    
glGA SDK v2021.0.5 ECSS (Entity Component System in a Scenegraph)
@Coopyright 2020-2021 George Papagiannakis
    
The classes below are all related to the GUI and Display part of the SDK
"""



import unittest
import time
import numpy as np

from pyglGA.GUI.Viewer import SDL2Decorator, SDL2Window, ImGUIDecorator
class TestSDL2Window(unittest.TestCase):
    
    def setUp(self):
        """[summary]
        """
        self.gWindow = SDL2Window()
        self.gContext = SDL2Decorator(self.gWindow)
        #self.gGUI = ImGUIDecorator(self.gContext)
    
    def test_init(self):
        """
        
        """
        print("TestSDL2Window:test_init START".center(100, '-'))
        
        self.gContext.init()
        #self.gGUI.init()
        
        self.assertIsNotNone(self.gWindow)
        self.assertIsNotNone(self.gContext)
        #self.assertIsNotNone(self.gGUI)
        self.assertIsInstance(self.gContext, SDL2Decorator)
        #self.assertIsInstance(self.gGUI, ImGUIDecorator)
        
        print("TestSDL2Window:test_init START".center(100, '-'))
        
        

if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=3, exit=False)