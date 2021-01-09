"""
Scene classes, part of the glGA SDK ECS
    
glGA SDK v2020.1 ECS (Entity Component System)
@Coopyright 2020 George Papagiannakis
    
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

from Entity import *
from Component import *
from System import *

class SingletonI(ABC):
    pass

class Scene(SingletonI):
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            print('Creating Scene Object')
            cls._instance = super(Scene, cls).__new__(cls)
            # add further init here
        return cls._instance
    
    def init():
        pass
    
    def update():
        pass
    
    def processInput():
        pass
        
    def render():
        pass
    
    def run():
        pass

if __name__ == "__main__":
    # The client code.

    s1 = Scene()
    s2 = Scene()

    if id(s1) == id(s2):
        print("Singleton works, both variables contain the same instance.")
    else:
        print("Singleton failed, variables contain different instances.")
        
    # create the basic Chapter 8 Hierarchy example from Angel ICG book
    
    base = EntityElement(1)
    arm = EntityElement(2)
    forearm = EntityElement(3)
    
    baseShape = EntityElement(4)
    armShape = EntityElement(5)
    forearmShape = EntityElement(6)
    
    base.add(arm)
    base.add(baseShape)
    arm.add(forearm)
    arm.add(armShape)
    forearm.add(forearmShape)
    
    scenegraph = base.update()
    
    print("Scenegraph is: ", scenegraph)
