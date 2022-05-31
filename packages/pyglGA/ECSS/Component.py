"""
Component classes, part of the glGA SDK ECSS
    
glGA SDK v2021.0.5 ECSS (Entity Component System in a Scenegraph)
@Coopyright 2020-2021 George Papagiannakis
    
The Compoment class is the dedicated to a specific type of data container in the glGA ECSS.

Based on the Composite and Iterator design patterns:
	• https://refactoring.guru/design-patterns/composite
    • https://github.com/faif/python-patterns/blob/master/patterns/structural/composite.py
    • https://refactoring.guru/design-patterns/iterator
    • https://github.com/faif/python-patterns/blob/master/patterns/behavioral/iterator.py

The following is example restructured text doc example
:param file_loc: The file location of the spreadsheet
:type file_loc: str
:returns: a list of strings representing the header columns
:rtype: list

"""

from __future__         import annotations
from abc                import ABC, abstractmethod
from math import atan2
from typing             import List
from collections.abc    import Iterable, Iterator

import pyglGA.ECSS.System
import uuid  
import pyglGA.ECSS.utilities as util


class Component(ABC, Iterable):
    """
    The Interface Component class of our ECSS.
    
    Based on the Composite pattern, it is a data collection of specific
    class of data. 
    Concrete Subclass Components typically are e.g. BasicTransform, RenderMesh, Shader, RigidBody etc.
    """
    
    def __init__(self, name=None, type=None, id=None):
        
        if (name is None):
            self._name = self.getClassName()
        else:
            self._name = name
        
        if (type is None):
            self._type = self.getClassName()
        else:
            self._type = type
        
        if id is None:
            self._id = uuid.uuid1().int #assign unique ID on Component
        else:
            self._id = id
        
        self._parent = self
        self._children = None
        self._worldManager = None
        self._eventManager = None
    
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
        
    @property #ECSSManager
    def worldManager(self):
        """ Get Component's ECSSManager """
        return self._worldManager
    @worldManager.setter
    def worldManager(self, value):
        self._worldManager = value
    
    @property #EventManager
    def eventManager(self):
        """ Get Component's EventManager """
        return self._eventManager
    @eventManager.setter
    def eventManager(self, value):
        self._eventManager = value
    
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
        raise NotImplementedError
    
    @abstractmethod
    def update(self, **kwargs):
        """
        method to be subclassed for debuging purposes only, 
        in case we need some behavioral or logic computation within te Component. 
        This violates the ECS architecture and should be avoided.
        """
        raise NotImplementedError
    
    @abstractmethod
    def accept(self, system: pyglGA.ECSS.System, event = None):
        """
        Accepts a class object to operate on the Component, based on the Visitor pattern.

        :param system: [a System object]
        :type system: [System]
        """
        raise NotImplementedError
                
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


class ComponentDecorator(Component):
    """Basic Component Decorator, based on the Decorator design pattern

    :param Component: [description]
    :type Component: [type]
    :return: [description]
    :rtype: [type]
    """
    
    def __init__(self, comp, name=None, type=None, id=None):
        super().__init__(name, type, id)
        self._component = comp
    
    @property
    def component(self):
        return self._component
    
    def init(self):
        self._component.init()
    
    def update(self, **kwargs):
        self._component.update(**kwargs)
    
    #def accept(self, system: pyglGA.ECSS.System):
       # we want the decorator first to accept the visitor and only if needed the wrappe to accept it too
       # each component decorator has to override this method
        
    
    

class ComponentIterator(ABC):
    """Abstract component Iterator class

    :param ABC: [description]
    :type ABC: [type]
    :return: [description]
    :rtype: [type]
    """
    pass

class CompNullIterator(Iterator, ComponentIterator):
    """
    The Default Null iterator for a Concrete Component class

    :param Iterator: [description]
    :type Iterator: [type]
    """
    def __init__(self, comp: Component):
        self._comp = comp
    
    def __next__(self):
        return None
    

class BasicTransform(Component):
    """
    An example of a concrete Component Transform class
    
    Contains a basic Euclidean Translation, Rotation and Scale Homogeneous matrices
    all-in-one TRS 4x4 matrix
    
    :param Component: [description]
    :type Component: [type]
    """
   
    def __init__(self, name=None, type=None, id=None, trs=None):
        
        super().__init__(name, type, id)
        
        if (trs is None):
            self._trs = util.identity()
        else:
            self._trs = trs
            
        self._l2world = util.identity()
        self._l2cam = util.identity()
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
        """ Get Component's local to world transform: translation, rotation ,scale """
        return self._l2world
    @l2world.setter
    def l2world(self, value):
        self._l2world = value
        
    @property #l2cam
    def l2cam(self):
        """ Get Component's local to camera transform: translation, rotation ,scale, projection """
        return self._l2cam
    @l2cam.setter
    def l2cam(self, value):
        self._l2cam = value                 

    @property #translation vector
    def translation(self):
        return self.trs[:3,3];
    @property #rotation vector
    def rotationEulerAngles(self):
        # First get rotation matrix from trs. Divide by scale
        rotationMatrix = self.trs.copy();
        rotationMatrix[:][0] /= self.scale[0];
        rotationMatrix[:][1] /= self.scale[1];
        rotationMatrix[:][2] /= self.scale[2];
        # Now, extract euler angles from rotation matrix
        x = atan2(rotationMatrix[1][2], rotationMatrix[2][2]);
        y = 0;
        z = 0;
        return [x, y, z];
    @property #scale vector
    def scale(self):
        x = self.trs[0, 0];
        y = self.trs[1, 1];
        z = self.trs[2, 2];
        return [x, y, z];

    def update(self, **kwargs):
        """ Local 2 world transformation calculation
        Traverses upwards whole scenegraph and multiply all transformations along this path
        
        Arguments could be "l2world=" or "trs=" or "l2cam=" to set respective matrices 
        """
        print(self.getClassName(), ": update() called")
        arg1 = "l2world"
        arg2 = "trs"
        arg3 = "l2cam"
        if arg1 in kwargs:
            print("Setting: ", arg1," with: \n", kwargs[arg1])
            self._l2world = kwargs[arg1]
        if arg2 in kwargs:
            print("Setting: ", arg2," with: \n", kwargs[arg2])
            self._trs = kwargs[arg2]
        if arg3 in kwargs:
            print("Setting: ", arg3," with: \n", kwargs[arg3])
            self._l2cam = kwargs[arg3]
        
    def accept(self, system: pyglGA.ECSS.System, event = None):
        """
        Accepts a class object to operate on the Component, based on the Visitor pattern.

        :param system: [a System object]
        :type system: [System]
        """
        
        system.apply2BasicTransform(self) #from TransformSystem
        system.applyCamera2BasicTransform(self) #from CameraSystem
        """
        if (isinstance(system, System.TransformSystem)):
            system.apply(self)
        
        if (isinstance(system, System.CameraSystem)):
            system.applyCamera(self)
        """
    
    def init(self):
        """
        abstract method to be subclassed for extra initialisation
        """
        pass

    def __str__(self):
        return f"\n {self.getClassName()} name: {self._name}, type: {self._type}, id: {self._id}, parent: {self._parent._name}, \nl2world: \n{self.l2world}, \nl2cam: \n{self.l2cam}, \ntrs: \n{self.trs}"
    
    def __iter__(self) ->CompNullIterator:
        """ A concrete component does not have children to iterate, thus a NULL iterator
        """
        return CompNullIterator(self) 
class Camera(Component):
    """
    An example of a concrete Component Camera class
    
    Contains a basic Projection matrices (otrhographic or perspective)
    
    :param Component: [description]
    :type Component: [type]
    """
   
    def __init__(self, projMatrix=None, name=None, type=None, id=None, left=-100.0, right=100.0, bottom=-100.0, top=100.0, near=1.0, far=100.0):
        super().__init__(name, type, id)
        
        if projMatrix is not None:
            self._projMat = projMatrix
        else:
            self._projMat = util.ortho(left, right, bottom, top, near, far)
        self._root2cam = util.identity()
        self._parent = self
         
    @property #projMat
    def projMat(self):
        """ Get Component's camera Projection matrix """
        return self._projMat
    @projMat.setter
    def projMat(self, value):
        self._projMat = value
    
    @property #_root2cam
    def root2cam(self):
        """ Get Component's root to camera matrix """
        return self._root2cam
    @root2cam.setter
    def orthoroot2camMat(self, value):
        self._root2cam = value                   
    
    def update(self, **kwargs):
        """ Update Camera matrices
        
        Arguments could be "root2cam=" to set respective matrices 
        """
        print(self.getClassName(), ": update() called")
        arg1 = "root2cam"
        if arg1 in kwargs:
            print("Setting: ", arg1," with: \n", kwargs[arg1])
            self._root2cam = kwargs[arg1]  
       
    def accept(self, system: pyglGA.ECSS.System, event = None):
        """
        Accepts a class object to operate on the Component, based on the Visitor pattern.

        :param system: [a System object]
        :type system: [System]
        """
        
        # In Python due to ducktyping, either call a System concrete method
        # or leave it generic as is and check within System apply() if the 
        #correct node is visited (there is no automatic inference which System to call 
        # due to its type. We need to call a System specific concrete method otherwise)
        system.apply2Camera(self)
    
    def init(self):
        """
        abstract method to be subclassed for extra initialisation
        """
        pass
    
    def __str__(self):
        return f"\n {self.getClassName()} name: {self._name}, type: {self._type}, id: {self._id}, parent: {self._parent._name}, \n projMat: \n{self.projMat},\n root2cam: \n{self.root2cam}"    

    def __iter__(self) ->CompNullIterator:
        """ A component does not have children to iterate, thus a NULL iterator
        """
        return CompNullIterator(self) 

class RenderMesh(Component):
    """
    A concrete RenderMesh class

    Accepts a dedicated RenderSystem to initiate rendering of the RenderMesh, using its vertex attributes (property)
    """
    def __init__(self, name=None, type=None, id=None, vertex_attributes=None, vertex_index=None):
        """ Initialize the generic RenderMesh component with the vertex attribute arrays
        this is the generic place to store all vertex attributes (vertices, colors, normals, bone weights etc.)
        specifically for OpenGL buffers, these will be passed to a VertexArray by a RenderGLShaderSystem
        then other RenderSystems could use that vertex attribute information for their rendering, 
        e.g. a RenderRayTracingSystem for backwards rayTracing, a RenderPathTracingSystem for pathTracing etc. 

        """
        super().__init__(name, type, id)
        
        self._parent = self
        if not vertex_attributes:
            self._vertex_attributes = [] #list of vertex attribute lists 
        else:
            self._vertex_attributes = vertex_attributes
            
        if not vertex_index:
                self.vertex_index = [] #list of vertex attribute lists 
        else:
            self._vertex_index = vertex_index
    
    @property
    def vertex_attributes(self):
        return self._vertex_attributes
    
    @vertex_attributes.setter
    def vertex_attributes(self, value):
        self._vertex_attributes = value
    
    @property
    def vertex_index(self):
        return self._vertex_index
    
    @vertex_index.setter
    def vertex_index(self, value):
        self._vertex_index = value
        
    def update(self):
        print(self.getClassName(), ": update() called")
   
   
    def accept(self, system: pyglGA.ECSS.System, event = None):
        """
        Accepts a class object to operate on the Component, based on the Visitor pattern.

        :param system: [a System object]
        :type system: [System]
        """
        system.apply2RenderMesh(self)
    
    
    def init(self):
        """
        abstract method to be subclassed for extra initialisation
        """
        pass
    
    def print(self):
        """
        prints out name, type, id, parent of this Component
        """
        print(f"\n {self.getClassName()} name: {self._name}, type: {self._type}, id: {self._id}, parent: {self._parent._name}, vertex_attributes: \n{self._vertex_attributes}")
        print(f" ______________________________________________________________")
    
    
    def __str__(self):
        return f"\n {self.getClassName()} name: {self._name}, type: {self._type}, id: {self._id}, parent: {self._parent._name}, vertex_attributes: \n{self._vertex_attributes}"

    
    def __iter__(self) ->CompNullIterator:
        """ A component does not have children to iterate, thus a NULL iterator
        """
        return CompNullIterator(self) 
    
    
class BasicTransformDecorator(ComponentDecorator):
    """An example of a concrete Component Decorator that wraps the component (BasicTransform) 
        and adds extra layered functionality 

    :param ComponentDecorator: [description]
    :type ComponentDecorator: [type]
    """
    def init(self):
        """
        example of a decorator
        """
        self.component.init()
        #call any extra methods before or after
    
    def accept(self, system: pyglGA.ECSS.System, event = None):
        pass # we want the decorator first to accept the visitor and only if needed the wrappe to accept it too
        #self._component.accept(system)