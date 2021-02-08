"""
Component classes, part of the glGA SDK ECS
    
glGA SDK v2020.1 ECS (Entity Component System)
@Coopyright 2020 George Papagiannakis
    
The Compoment class is the dedicated to a specific type of data container in the glGA ECS.

The following is example restructured text doc example
:param file_loc: The file location of the spreadsheet
:type file_loc: str
:returns: a list of strings representing the header columns
:rtype: list

"""

from __future__         import annotations
from abc                import ABC, abstractmethod
from typing             import List
from collections.abc    import Iterable, Iterator

from System     import *
from utilities  import *


class Component(ABC, Iterable):
    """
    The Interface Component class of our ECSS.
    
    Based on the Composite pattern, it is a data collection of specific
    class of data. 
    Concrete Subclass Components typically are e.g. BasicTransform, RenderMesh, Shader, RigidBody etc.
    """
    
    def __init__(self, name=None, type=None, id=None):
        self._name = name
        self._type = type
        self._id = id
        self._parent = self
        self._children = None
    
    #define properties for id, name, type, parent
    @property #name
    def name(self) -> str:
        """ Get Component's name """
        return self._name
    @name.setter
    def name(self, value):
        self._name = value
        
    @property #type
    def type(self) -> str:
        """ Get Component's type """
        return self._type
    @type.setter
    def type(self, value):
        self._type = value
        
    @property #id
    def id(self) -> int:
        """ Get Component's id """
        return self._id
    @id.setter
    def id(self, value):
        self._id = value
        
    @property #parent
    def parent(self) -> Component:
        """ Get Component's parent """
        return self._parent
    @parent.setter
    def parent(self, value):
        self._parent = value
    
    def add(self, object: Component) ->None:
        pass

    def remove(self, object: Component) ->None:
        pass
        
    def getChild(self, index) ->Component:
        return None
    
    def getNumberOfChildren(self) -> int:
        return len(self._children)
    
    @classmethod
    def getClassName(cls):
        return cls.__name__
    
    @abstractmethod
    def init(self):
        """
        abstract method to be subclassed for extra initialisation
        """
        pass
    
    @abstractmethod
    def update(self):
        """
        method to be subclassed for debuging purposes only, 
        in case we need some behavioral or logic computation within te Component. 
        This violates the ECS architecture and should be avoided.
        """
        pass
    
    @abstractmethod
    def accept(self, system: System):
        """
        Accepts a class object to operate on the Component, based on the Visitor pattern.

        :param system: [a System object]
        :type system: [System]
        """
        system.update()
        
    def print(self):
        """
        prints out name, type, id, parent of this Component
        """
        print(f"\n {self.getClassName()} name: {self._name}, type: {self._type}, id: {self._id}, parent: {self._parent._name}")
        print(f" ______________________________________________________________")
    
    def __iter__(self):
        """ Iterable method
        makes this abstract Component an iterable. It is meant to be overidden by subclasses.
        """
        return self 
    
    def __str__(self):
        return f"\n {self.getClassName()} name: {self._name}, type: {self._type}, id: {self._id}, parent: {self._parent._name}"


class CompNullIterator(Iterator):
    """
    The Default Null iterator for a Concrete Component class

    :param Iterator: [description]
    :type Iterator: [type]
    """
    def __init__(self, comp: Component):
        self._comp = comp
    
    def __next__(self):
        return None
    
    def hasNext(self)->bool:
        return False

class BasicTransform(Component):
    """
    An example of a concrete Component Transform class
    
    Contains a basic Euclidean Translation, Rotation and Scale Homogeneous matrices
    all-in-one TRS 4x4 matrix
    
    :param Component: [description]
    :type Component: [type]
    """
   
    def __init__(self, name=None, type=None, id=None):
        self._name = name
        self._type = type
        self._id = id
        self._trs = identity()
        self._l2world = identity()
        self._parent = self
        self._children = []
         
    @property #trs
    def trs(self):
        """ Get Component's transform: translation, rotation ,scale """
        return self._trs
    @trs.setter
    def trs(self, value):
        self._trs = value

    @property #l2world
    def l2world(self):
        """ Get Component's transform: translation, rotation ,scale """
        return self._l2world
    @l2world.setter
    def l2world(self, value):
        self._l2world = value                 
    
    def update(self):
        print(self.getClassName(), ": update() called")
    
    
    def accept(self, system: System):
        """
        Accepts a class object to operate on the Component, based on the Visitor pattern.

        :param system: [a System object]
        :type system: [System]
        """
        system.apply(self)
    
    
    def init(self):
        """
        abstract method to be subclassed for extra initialisation
        """
        pass
    
    def __iter__(self) ->CompNullIterator:
        """ A component does not have children to iterate, thus a NULL iterator
        """
        return CompNullIterator(self) 


class RenderMesh(Component):
    """
    A concrete RenderMesh class

    :param Component: [description]
    :type Component: [type]
    """
    def __init__(self, name=None, type=None, id=None):
        self._name = name
        self._type = type
        self._id = id
        self._trs = identity()
        self._parent = self
        self._children = []
    
    def draw(self):
        print(self.getClassName(), ": draw() called")
        
    def update(self):
        print(self.getClassName(), ": update() called")
        self.draw()
   
    def accept(self, system: System):
        """
        Accepts a class object to operate on the Component, based on the Visitor pattern.

        :param system: [a System object]
        :type system: [System]
        """
        system.apply(self)
    
    def init(self):
        """
        abstract method to be subclassed for extra initialisation
        """
        pass
    
    def __iter__(self) ->CompNullIterator:
        """ A component does not have children to iterate, thus a NULL iterator
        """
        return CompNullIterator(self) 
    