""" Entity classes, part of the glGA SDK ECS
    
glGA SDK v2020.1 ECS (Entity Component System)
@Coopyright 2020 George Papagiannakis
    
The Entity class is the based aggregation of Components in the glGA ECS.

The following is example restructured text doc example
:param file_loc: The file location of the spreadsheet
:type file_loc: str
:returns: a list of strings representing the header columns
:rtype: list

"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List

from Component import *

class Entity(ABC):
    """ The Interface  Entity abstract base class for all Entities
        The abstract methods update() and transform() contain logic that normally should be taken care by Systems 
        and are only provided here for debugging purposes only and should not be used, as in the ECS data-driven 
        methodology, Entities and Components contain data only and no logic.
    """
    
    def __init__(self, id=None):
        self._parent = None
        self._id = id
    
    @property
    def parent(self) -> Entity:
        return self._parent
    
    @parent.setter
    def parent(self, value):
        self._parent = value
    
    def add(self, object: Entity) ->None:
        pass
    
    def remove(self, object: Entity) ->None:
        pass
    
    def isEntity(self) -> bool:
        return False
    
    @abstractmethod
    def update(self) -> str:
        pass
    
    @abstractmethod
    def transform(self) -> bool:
        pass


class EntityElement(Entity):
    """
    The main Entity concrete class of glGA ECS 
    This is the typical equivalent of a Group node in traditional scenegraphs or GameObject in Unity Engine
    It can contain several other EntityElement objects as children. 
    It is an actual data aggregator container of Components. All the actuall operations and logic is performed by 
    Systems and not the Components or EntityElement itself.
    """

    def __init__(self, id=None) -> None:
        """
        PEP 256 
        note this is how we declare the type of variables in Phython 3.6 and later.
        e.g. x: int=1 or x: List[int] = [1] 
        """
        self._children: List[Entity]=[]
        self._components: List[Component]=[]
        self._id = id 

    def add(self, object: Entity) ->None:
        self._children.append(object)
        object._parent = self

    def remove(self, object: Entity) ->None:
        self._children.remove(object)
        object._parent = None
        
    def getChild(self, index) ->Entity:
        if index < len(self._children):
            return self._children[index]
    
    def getNumberOfChildren(self) -> int:
        return len(self._children)
    
    def addComponent(self, comp: Component) ->None:
        self._components.append(comp)
        
    def getComponent(self, index) -> Component:
        if index < len(self._components):
            return self._components[index]
        else:
            return None
    
    def removeComponent(self, comp: Component) -> None:
        self._components.remove(comp)
    
    def isEntity(self) -> bool:
        return True
    
    def update(self) ->str:
        """" Traverse recursively all children, call their update and print their representation """
        scene = []
        for child in self._children:
            scene.append(child.update())
        return f"{self._id} <- {''.join(scene)}"
    
    
    def transform(self)->bool:
        """ Sample transform() only for subclassing here and debug purposes """
        return False