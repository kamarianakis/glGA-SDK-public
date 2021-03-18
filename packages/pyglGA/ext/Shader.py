"""
Shader classes, extension of the glGA SDK ECSS
    
glGA SDK v2021 ECSS (Entity Component System in a Scenegraph)
@Coopyright 2020-2021 George Papagiannakis
    
The Shader Compoment class is the dedicated to a specific type of data container in the pyglGA ECSS
that of assembling, using and destroying OpenGL API shader programs

Based on the Composite and Iterator design patterns:
	• https://refactoring.guru/design-patterns/composite
    • https://github.com/faif/python-patterns/blob/master/patterns/structural/composite.py
    • https://refactoring.guru/design-patterns/iterator
    • https://github.com/faif/python-patterns/blob/master/patterns/behavioral/iterator.py


"""

from __future__         import annotations
from abc                import ABC, abstractmethod
from typing             import List
from collections.abc    import Iterable, Iterator

import pyglGA.ECSS.System
from pyglGA.ECSS.Component import Component, BasicTransform, Camera, RenderMesh, CompNullIterator, BasicTransformDecorator
import uuid  
import pyglGA.ECSS.utilities as util


class Shader(Component):
    """
    A concrete Shader class

    :param Component: [description]
    :type Component: [type]
    """
    def __init__(self, name=None, type=None, id=None):
        super().__init__(name, type, id)
        
        self._trs = util.identity()
        self._parent = self
        self._children = []
    
    def draw(self):
        print(self.getClassName(), ": draw() called")
        
    def update(self):
        print(self.getClassName(), ": update() called")
        self.draw()
   
    def accept(self, system: pyglGA.ECSS.System):
        """
        Accepts a class object to operate on the Component, based on the Visitor pattern.

        :param system: [a System object]
        :type system: [System]
        """
        system.apply2Shader(self)
    
    def init(self):
        """
        abstract method to be subclassed for extra initialisation
        """
        pass
    
    def __iter__(self) ->CompNullIterator:
        """ A component does not have children to iterate, thus a NULL iterator
        """
        return CompNullIterator(self) 