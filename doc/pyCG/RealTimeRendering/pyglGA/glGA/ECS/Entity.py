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

class EntityDfsIterator(Iterator):
    """
    This is a depth-first-iterator for Hierarchical Entities (Iterables) and their Components, 
    based on the Iterator design pattern

    :param Iterator: [description]
    :type Iterator: [type]
    """
            
    # List stack to push/pop iterators
            
    def __init__(self, entity: Entity) ->None:
        self._entity = entity
        self._children = entity._children
        # access top level Entity List iterator
        self._entityIterator = iter(entity._children)
        self._stack: List[Iterator] = []
        # store top level Entity List iterator in stack
        self._stack.append(self._entityIterator)
        self._hasnext = None
        
    def peek(self)->Iterator:
        """ Stack peek over
        
            just access last stack LIFO element without removing it
        """
        if (len(self._stack) == 0):
            return None
        else:
            return self._stack[-1]
                    
    def __next__(self):
        """
        The __next__() iterator method should return the next Entity in the graph, using a DFS algorithm.
        """
        if (self.hasNext()):
            # if there is a next element, get current iterator off the stack and get its next element
            eIterator = self.peek()
            component = next(eIterator)
            
            # we throw that component's iterator in the stack. If the component is an Entity, it will iterate
            # over its items. If the component is a concrete Component, we get CompNullIterator, no iteration 
            # happens. Then we return the component
            self._stack.append(iter(component))

            return component
        else:
            return None
    
    def hasNext(self) ->bool:
        """
        Peak to see if there is a next element to access
        """
        # to see if there is a next element, we check to see if the stack is empty; if so, there isn't
        if (len(self._children) == 0): 
            return False
        else:
            eIterator = self.peek()
            if (not self.list_hasNext(eIterator)): #Our Python implementation of a standard List iterator hasNext()
                self._stack.pop()
                return self.hasNext()
            else:
                return True
    
    
    def list_hasNext(self, iter) ->bool:
        """ Python List iterator hasNext() implementation
        Standard iterators in Python lack hasNext(), so here is a simple implementation
        """
        if self._hasnext is None:
            try: 
                next(iter)
            except StopIteration: 
                self._hasnext = False
            else: 
                self._hasnext = True
        return self._hasnext

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
        self._parent = self
    
    
    def print(self):
        """
        Print out contents of Entity for Debug purposes only
        """
        #print out name, type, id of this Entity
        print(f"\n {self.getClassName()} name: {self._name}, type: {self._type}, id: {self._id}, parent: {self._parent._name}")
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
        
    
    
    