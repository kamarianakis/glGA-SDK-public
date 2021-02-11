"""
System classes, part of the glGA SDK ECS
    
glGA SDK v2020.1 ECS (Entity Component System)
@Coopyright 2020 George Papagiannakis
    
The System class is the logic-specific processor of different Components in the glGA ECS.

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
from Entity import *

class System(ABC):
    """
    Main abstract class of the System part of our ECS
    
    Typically involves all logic involving operations such as Rendering, Local2World, Physics

    :param ABC: [description]
    :type ABC: [type]
    """
    
    def __init__(self, name=None, type=None, id=None):
        self._name = name
        self._type = type
        self._id = id
    
    #define properties for id, name, type
     
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
    def id(self) -> str:
        """ Get Component's id """
        return self._id
    @id.setter
    def id(self, value):
        self._id = value
    
    @classmethod
    def getClassName(cls):
        return cls.__name__
    
    def update(self):
        """
        method to be subclassed for  behavioral or logic computation 
        when visits Components of an EntityNode. 
        
        """
        pass
    
    def apply(self, Entity):
        """
        method to be subclassed for  behavioral or logic computation 
        when visits Entities. 
        
        """
        pass
    
    
    def apply(self, renderMesh: RenderMesh):
        """
        method to be subclassed for  behavioral or logic computation 
        when visits Components. 
        
        """
        pass
    
    
    def apply(self, basicTransform: BasicTransform):
        """
        method to be subclassed for  behavioral or logic computation 
        when visits Components. 
        
        """
        pass


class TransformSystem(System):
    """

    :param System: [description]
    :type System: [type]
    :return: [description]
    :rtype: [type]
    """
    
    def __init__(self, name=None, type=None, id=None, cameraComponent=None):
        self._name = name
        self._type = type
        self._id = id
        self._camera = cameraComponent #if Scene has a cameraComponent, specify also l2Camera
        
    
    def update(self):
        """
        method to be subclassed for  behavioral or logic computation 
        when visits Components of an EntityNode. 
        
        """
        pass
    
    def getLocal2World(self, leafComp: Component, topComp=None):
        """Calculate the l2world BasicTransform matrix

        :param leafComp: [description]
        :type leafComp: Component
        :param topComp: [description], defaults to None
        :type topComp: [type], optional
        :return: the local2world matrix of the visited BasicTransform
        :rtype: numpy.array
        """
        
        # get parent Entity this BasicTransform Component belongs to
        componentEntity = leafComp.parent
        topAccessedEntity = componentEntity
        parentTRS = identity()
        l2worldTRS = leafComp.l2world
        # while (p1._parent is not None)
        while(componentEntity is not topComp):
            # get that parent's TRS by type
            parentBasicTrans = componentEntity.getChildByType("BasicTransform")
            if(parentBasicTrans is not None):
                parentTRS = parentBasicTrans.trs
                # l2world = multiply current with parent's TRS 
                l2worldTRS = l2worldTRS @ parentBasicTrans.trs
            topAccessedEntity = componentEntity
            componentEntity = componentEntity.parent
        else: #parent is now the root node, so check if it has a Transform component
            parentBasicTrans = topAccessedEntity.getChildByType("BasicTransform")
            if(parentBasicTrans is not None):
                parentTRS = parentBasicTrans.trs
                # l2world = multiply current with parent's TRS 
                l2worldTRS = l2worldTRS @ parentBasicTrans.trs
                
        return l2worldTRS
        
        
    
    def apply(self, basicTransform: BasicTransform):
        """
        method to be subclassed for  behavioral or logic computation 
        when visits Components. 
        
        In this case calculate the l2w BasicTransform component matrix
        
        """
        print(self.getClassName(), ": apply(BasicTransform) called")
        
        # getLocal2World returns result to be set in BasicTransform::update(**kwargs) below
        l2worldTRS = self.getLocal2World(basicTransform)
        #update l2world of basicTransform
        basicTransform.update(l2world=l2worldTRS) 


class RenderSystem(System):
    """
    A basic forward rendering system based on GPU shaders
    :param System: [description]
    :type System: [type]
    """
    
    def update(self):
        """
        method to be subclassed for  behavioral or logic computation 
        when visits Components of an EntityNode. 
        
        """
        pass
    
    
    def apply(self, renderMesh: RenderMesh):
        """
        method to be subclassed for  behavioral or logic computation 
        when visits Components. 
        
        """
        print(self.getClassName(), ": apply(RenderMesh) called")
        renderMesh.update()
    
    
            
