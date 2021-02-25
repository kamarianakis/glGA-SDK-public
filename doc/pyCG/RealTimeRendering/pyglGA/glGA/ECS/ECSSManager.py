"""
ECSSManager, part of the glGA SDK ECSS
    
glGA SDK v2020.1 ECS (Entity Component System)
@Coopyright 2020 George Papagiannakis

"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Dict

from Entity import Entity



class ECSSManager():
    """
    Singleton Manager class to provide factory creation methods for
    all Entities, Components, Systems, as an alternative way and hide the scenegraph complexity.

    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            print('Creating Scene Singleton Object')
            cls._instance = super(ECSSManager, cls).__new__(cls)
            # add further init here
        return cls._instance

    def __init__(self):
        self._systems = []
        self._entities = {}
        self._components = {}
        self._next_entity_id = 0


    def createEntity(self):
        pass
    
    
    def addComponent(self):
        pass
    
    
    def addSystem(self):
        pass
    
    
    def addEntityChild(self):
        pass


if __name__ == "__main__":
    # The client code.

    s1 = ECSSManager()
    s2 = ECSSManager()
    
    if id(s1) == id(s2):
        print("Singleton works, both variables contain the same instance.")
    else:
        print("Singleton failed, variables contain different instances.")