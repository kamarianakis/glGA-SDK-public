""" Entity class, part of the glGA SDK ECS
    
glGA SDK v2020.1 ECS (Entity Component System)
@Coopyright 2020 Prof. George Papagiannakis
    
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

class Entity(ABC):
    """ The Interface  Entity abstract base class for all Entities
    """
    
    def __init__(self):
        self._parent = None
    
    
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
    def update(self) -> bool:
        return False
    
    @abstractmethod
    def transform(self) -> bool:
        return False


class SceneEntity(Entity):
    """the main Entity concrete class of glGA ECS 
    """
    def update(self) ->bool:
        return True
    
    def transform(self)->bool:
        return True