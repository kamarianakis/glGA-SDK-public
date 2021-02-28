"""
ECSSManager, part of the glGA SDK ECSS
    
glGA SDK v2020.1 ECS (Entity Component System)
@Coopyright 2020 George Papagiannakis

"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Dict

from Entity import Entity
import Component
import System
import utilities as util


class ECSSManager():
    """
    Singleton Manager class to provide factory creation methods for
    all Entities, Components, Systems, as an alternative way and hide the scenegraph complexity.

    """
    _instance = None
    
    def __new__(cls):
        """
        Special singleton class method, returns single instance of ECSSManager

        :return: single class instance
        :rtype: ECSSManagger
        """
        if cls._instance is None:
            print('Creating Scene Singleton Object')
            cls._instance = super(ECSSManager, cls).__new__(cls)
            # add further init here
        return cls._instance

    def __init__(self):
        """
        Construct initial data structures for scenegraph elements
        """
        self._systems: List[System.System]=[] #list for all systems
        self._components: List[Component.Component]=[] #list with all scenegraph components
        self._entities: List[Entity]=[] #list of all scenegraph entities
        self._cameras: List[Component.Component]=[] # list of all scenegraph camera components
        self._entities_components = {} #dict with keys entities and values list of components per entity
        self._next_entity_id = 0
        self._root = None

        

    def createEntity(self, entity: Entity):
        """
        Creates an Entity in the underlying scenegraph and adds it in the ECSS data structures.
        
        Checks if the Entity's name is "root" to add it as root of the ECSS
        
        :param entity: Entity to add in the Scenegraph
        :type entity: Entity
        """
        if isinstance(entity, Entity):
            self._entities.append(entity) #add an empty list for components with the new Entity
            self._entities_components[entity]=[None]
        
            if entity.name.lower() == "root":
                self._root = entity
        
        return entity #if the method was called with an inline constructor e.g. 'createEntity(Entity())', 
                        # we return that created Entity in case it is needed
    
    
    def createSystem(self, system: System.System):
        """
        Creates a System and adds it in the ECSS data structures
        
        """
        if isinstance(system, System.System):
            self._systems.append(system)
        
        return system
    
    
    def createIterator(self, entity: Entity, dfs=True):
        """
        Creates and returns a scenegraph traversal node iterator

        :param entity: [description]
        :type entity: Entity
        """
        if isinstance(entity, Entity):
            if dfs:
                return iter(entity)
        
        
    
    def addComponent(self, entity: Entity, component: Component.Component):
        """
        Adds a component to an Entity in a scenegraph and in the ECSS data structures
        
        Checks if that Component is a Camera, to add it in the list of Cameras
        
        Checks if that Entity has already such a component of that type and replaces 
        it with the new one
        
        Checks that indeed only a component is added with this method. 
        If we need to add a child Entity to an Enity, we use addEntityChild()

        :param entity: Parent Entity
        :type entity: Entity
        :param component: The component to be added to this Entity
        :type component: Component
        """
        pass
    
    
    def addEntityChild(self, entity_parent: Entity, entity_child: Entity):
        """
        Adds a child Enity to a parent one and thus establishes a hierarchy 
        in the underlying scenegraph.
        
        Adds the child Entity also in the ECSS _entities_components dictionary 
        data structure, so that the hierarchy is also visible at ECSSManager level.

        :param entity_parent: [description]
        :type entity_parent: Entity
        :param entity_child: [description]
        :type entity_child: Entity
        """
        pass


if __name__ == "__main__":
    # The client code.

    s1 = ECSSManager()
    s2 = ECSSManager()
    
    if id(s1) == id(s2):
        print("Singleton works, both variables contain the same instance.")
    else:
        print("Singleton failed, variables contain different instances.")