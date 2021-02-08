""" EntityI classes, part of the glGA SDK ECS
    
glGA SDK v2020.1 ECS (EntityI Component System)
@Coopyright 2020 George Papagiannakis
    
The EntityI class is the based aggregation of Components in the glGA ECS.

The following is example restructured text doc example
:param file_loc: The file location of the spreadsheet
:type file_loc: str
:returns: a list of strings representing the header columns
:rtype: list

"""

from __future__ import annotations
from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator
from typing import Any, List

from Component import *
from System import *
import copy


class EntityDfsIterator(Iterator):
    """
    This is a depth-first-iterator for Hierarchical Entities (Iterables) and their Components, 
    based on the Iterator design pattern

    :param Iterator: [description]
    :type Iterator: [type]
    """
            
    # List stack to push/pop iterators
            
    def __init__(self, entity: Entity) ->None:
        self._entity = entity #entity this iterator can access the children of
        
        # access underlying Entity List iterator
        self._entityIterator = iter(self._entity._children)
        self._stack: List[Iterator] = []
        
        # store top level Entity List iterator in stack
        self._stack.append(self._entityIterator)
                    
    def __next__(self):
        """
        The __next__() iterator method should return the next Entity in the graph, using a DFS algorithm.
        This is a "pythonic" iterator, based on standard python List iterators
        """
        if (len(self._stack) == 0): 
            raise StopIteration
        else:
            stackIter = self._stack[-1] # peak last stack element
            try:
                node = next(stackIter) # advance stack iterator to retrieve first child node in it
            except StopIteration:
                    self._stack.pop() # remove top iterator as it has been exhausted
                    return None
            else:
                if isinstance(node, Entity):
                    self._stack.append(iter(node._children)) # push the new Entity's iterator on top of the stack to be parsed next() iteration
                    return node #node is an Entity
                else: 
                    return node #node is Component
            
class Entity(Component):
    """
    The main EntityI concrete class of glGA ECS 
    This is the typical equivalent of a Group node in traditional scenegraphs or GameObject in Unity Engine
    It can contain several other Entity objects as children. 
    It is an actual data aggregator container of Components. All the actuall operations and logic is performed by 
    Systems and not the Components or Entity itself.
    """

    def __init__(self, name=None, type=None, id=None) -> None:
        """
        PEP 256 
        note this is how we declare the type of variables in Phython 3.6 and later.
        e.g. x: int=1 or x: List[int] = [1] 
        """
        self._children: List[Component]=[]
        self._name = name
        self._type = type
        self._id = id
        self._parent = None
    
    
    def print(self):
        """
        Print out contents of Entity for Debug purposes only
        """
        #print out name, type, id of this Entity
        if (self._parent is not None): #in case this is not the root node
            print(f"\n {self.getClassName()} name: {self._name}, type: {self._type}, id: {self._id}, parent: {self._parent._name}")
        else:
            print(f"\n {self.getClassName()} name: {self._name}, type: {self._type}, id: {self._id}, parent: None (root node)")

        print(f" --------------------------------------------------- ")
        #create a local iterator of Entity's children
        debugIterator = iter(self._children)
        #call print() on all children (Concrete Components or Entities) while there are more children to traverse
        done_traversing = False
        while not done_traversing:
            try:
                comp = next(debugIterator)
            except StopIteration:
                done_traversing = True
            else:
                comp.print()

    def add(self, object: Component) ->None:
        self._children.append(object)
        object._parent = self

    def remove(self, object: Component) ->None:
        self._children.remove(object)
        object._parent = None
        
    def getChild(self, index) ->Component:
        if index < len(self._children):
            return self._children[index]
        else:
            return None
    
    def getNumberOfChildren(self) -> int:
        return len(self._children)
    
    
    def isEntity(self) -> bool:
        return True
    
    def update(self) ->str:
        pass
    
    def transform(self)->bool:
        """ Sample transform() only for subclassing here and debug purposes """
        return False
        ""
    
    def accept(self, system: System):
        """
        Accepts a class object to operate on the Component, based on the Visitor pattern.

        :param system: [a System object]
        :type system: [System]
        """
        system.update()
    
    def init(self):
        """
        abstract method to be subclassed for extra initialisation
        """
        pass
    
    def __iter__(self) -> EntityDfsIterator: 
        """
        The __iter__() method normaly returns the iterator object itself, by default
        we return the depth-first-search iterator
        """
        return EntityDfsIterator(self)
    
    def __str__(self):
        if (self._parent is not None): #in case this is not the root node
            return f"\n {self.getClassName()} name: {self._name}, type: {self._type}, id: {self._id}, parent: {self._parent._name}"
        else:
            return f"\n {self.getClassName()} name: {self._name}, type: {self._type}, id: {self._id}, parent: None (root node)"

        
    
    
    