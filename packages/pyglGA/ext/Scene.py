"""
Scene classes, part of the glGA SDK ECSS
    
glGA SDK v2021.0.5 ECSS (Entity Component System in a Scenegraph)
@Coopyright 2020-2021 George Papagiannakis
    
The Compoment class is the dedicated to a specific type of data container in the glGA ECS.

The following is example restructured text doc example
:param file_loc: The file location of the spreadsheet
:type file_loc: str
:returns: a list of strings representing the header columns
:rtype: list

"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Dict

import numpy as np

import pyglGA.ECSS.utilities as util
from pyglGA.ECSS.Entity import Entity, EntityDfsIterator
from pyglGA.ECSS.Component import BasicTransform, Camera
from pyglGA.ECSS.System import System, TransformSystem, CameraSystem, RenderSystem
from pyglGA.ECSS.ECSSManager import ECSSManager
from pyglGA.GUI.Viewer import SDL2Window, ImGUIDecorator

class Scene():
    """
    Singleton Scene that assembles ECSSManager and Viewer classes together for Scene authoring
    in pyglGA
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            print('Creating Scene Singleton Object')
            cls._instance = super(Scene, cls).__new__(cls)
            # add further init here
        return cls._instance
    
    
    def __init__(self):
        self._renderWindow = None
        self._world = ECSSManager()
    
    @property
    def renderWindow(self):
        return self._renderWindow
    
    @property
    def world(self):
        return self._world
    
    
    def init(self, sdl2 = True, imgui = False):
        """call the init() of all systems attached to this Scene based on the Visitor pattern
        """
        gContext = None
        
        if sdl2 == True:
            gWindow = SDL2Window()
            gContext = gWindow
        
        if imgui == True:
            gGUI = ImGUIDecorator(gWindow)
            gContext = gWindow
    
        gContext.init()
        gContext.init_post()
    
    
    def update(self):
        """call the update() of all systems attached to this Scene based on the Visitor pattern
        """
        pass
    
    
    def processInput(self):
        """process the user input per frame based on Strategy and Decorator patterns
        """
        pass
    
        
    def render(self):
        """call the render() of all systems attached to this Scene based on the Visitor pattern
        """
        pass
    
    
    def run(self):
        """main loop Scene method based on the "gameloop" game programming pattern
        """
        pass


if __name__ == "__main__":
    # The client singleton code.

    s1 = Scene()
    s2 = Scene()

    if id(s1) == id(s2):
        print("Singleton works, both Scenes contain the same instance.")
    else:
        print("Singleton failed, Scenes contain different instances.")
        