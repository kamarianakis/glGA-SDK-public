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

import sys
from pathlib import Path


from ...pyglGA.ECSS.Entity import Entity


class SingletonI(ABC):
    pass

class Scene(SingletonI):
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            print('Creating Scene Singleton Object')
            cls._instance = super(Scene, cls).__new__(cls)
            # add further init here
        return cls._instance
    
    def init():
        """call the init() of all systems attached to this Scene based on the Visitor pattern
        """
        pass
    
    def update():
        """call the update() of all systems attached to this Scene based on the Visitor pattern
        """
        pass
    
    def processInput():
        """process the user input per frame based on Strategy and Decorator patterns
        """
        pass
        
    def render():
        """call the render() of all systems attached to this Scene based on the Visitor pattern
        """
        pass
    
    def run():
        """main loop Scene method based on the "gameloop" game programming pattern
        """
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
    
    base = Entity("base", "group", 1)
    arm = Entity("arm", "group",2)
    forearm = Entity("forearm", "group",3)
    
    baseShape = Entity("baseShape", "shape",4)
    armShape = Entity("armShape", "shape", 5)
    forearmShape = Entity("forearmShape", "shape", 6)
    
    base.add(arm)
    base.add(baseShape)
    arm.add(forearm)
    arm.add(armShape)
    forearm.add(forearmShape)
    
    #scenegraph = base.update()
    #print("Scenegraph is: ", scenegraph)
    # ----------- attach a render system to root Entity ---------------
    # 
    #
    print(f"----------- attached a render system to root Entity: {base._name} ---------------")
    
    # ----------- run a render system from root Entity towards leaf nodes (DFS) and compute l2world matrix ---------------
   
