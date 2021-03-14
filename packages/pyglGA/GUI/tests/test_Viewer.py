"""
Test Viewer classes, part of the pyglGA SDK ECSS
    
glGA SDK v2021.0.5 ECSS (Entity Component System in a Scenegraph)
@Coopyright 2020-2021 George Papagiannakis
    
The classes below are all related to the GUI and Display part of the SDK
"""



import unittest
import time
import numpy as np

from pyglGA.GUI.Viewer import SDL2Window, ImGUIDecorator
class TestSDL2Window(unittest.TestCase):
    
    def setUp(self):
        """[summary]
        """
        self.gWindow = SDL2Window()
        self.gGUI = ImGUIDecorator(self.gWindow)
    
    @unittest.skip("test_initSDL2Decorator or test_initSDL2Decorator, skipping the test")
    def test_initSDL2Decorator(self):
        """
        Running the basic RenderWindow with the concrete basic Compoment of the decorator
        patter, that is the SDL2Window, without any decorator on top
        """
        print("TestSDL2Window:test_initSDL2Decorator START".center(100, '-'))
        
        self.gWindow.init()
        
        
        running = True
        # MAIN RENDERING LOOP
        while running:
            self.gWindow.display()
            running = self.gWindow.event_input_process(running)
            self.gWindow.display_post()
        self.gWindow.shutdown()
        
        self.assertIsNotNone(self.gWindow)
        self.assertIsInstance(self.gWindow, SDL2Window)
        
        print("TestSDL2Window:test_initSDL2Decorator START".center(100, '-'))
        
    def test_initImGUIDecorator(self):
        """
        
        """
        print("TestSDL2Window:test_initImGUIDecorator START".center(100, '-'))
        
        self.gGUI.init()
        
        running = True
        # MAIN RENDERING LOOP
        while running:
            self.gGUI.display()
            running = self.gGUI.event_input_process(running)
            self.gGUI.display_post()
        self.gGUI.shutdown()
        
        self.assertIsNotNone(self.gWindow)
        self.assertIsNotNone(self.gGUI)
        self.assertIsInstance(self.gWindow, SDL2Window)
        self.assertIsInstance(self.gGUI, ImGUIDecorator)
        
        print("TestSDL2Window:test_initImGUIDecorator START".center(100, '-'))

if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=3, exit=False)