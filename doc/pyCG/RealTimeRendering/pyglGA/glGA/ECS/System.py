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

import Component
import utilities as util

class System(ABC):
    """
    Main abstract class of the System part of our ECS
    
    Typically involves all logic involving operations such as: 
    Transform, Physics, Animation (simulation), Camera (cull), Rendering (draw) 
    traversals and logic operationls on Components and Entities
   
    :param ABC: [description]
    :type ABC: [type]
    """
    
    def __init__(self, name=None, type=None, id=None, priority=0):
        self._name = name
        self._type = type
        self._id = id
        self._priority = priority
    
    #define properties for id, name, type, priority
     
    @property #name
    def name(self) -> str:
        """ Get Systems's name """
        return self._name
    @name.setter
    def name(self, value):
        self._name = value
        
    @property #type
    def type(self) -> str:
        """ Get Systems's type """
        return self._type
    @type.setter
    def type(self, value):
        self._type = value
        
    @property #id
    def id(self) -> str:
        """ Get Systems's id """
        return self._id
    @id.setter
    def id(self, value):
        self._id = value
        
    @property #priority
    def priority(self) -> str:
        """ Get Systems's priority """
        return self._priority
    @priority.setter
    def priority(self, value):
        self._priority = value
    
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
    
    
    def apply(self, renderMesh: Component.RenderMesh):
        """
        method to be subclassed for  behavioral or logic computation 
        when visits Components. 
        
        """
        pass
    
    
    def apply(self, basicTransform: Component.BasicTransform):
        """
        method to be subclassed for  behavioral or logic computation 
        when visits Components. 
        
        """
        pass
    
    def applyCamera(self, basicTransform: Component.BasicTransform):
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
        parentTRS = util.identity()
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
        
        
    
    def apply(self, basicTransform: Component.BasicTransform):
        """
        method to be subclassed for  behavioral or logic computation 
        when visits Components. 
        
        In this case calculate the l2w BasicTransform component matrix
        
        """
        
        #check if the visitor visits a node that it should not
        if (isinstance(basicTransform,Component.BasicTransform)) == False:
            return #in Python due to duck typing we need to check this!
        print(self.getClassName(), ": apply(BasicTransform) called")
        
        # getLocal2World returns result to be set in BasicTransform::update(**kwargs) below
        l2worldTRS = self.getLocal2World(basicTransform)
        #update l2world of basicTransform
        basicTransform.update(l2world=l2worldTRS) 


class CameraSystem(System):
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
        
    def getRoot2Camera(self, leafComp: Component, topComp=None):
        """Calculate the root to camera matrix

        :param leafComp: [description]
        :type leafComp: Component
        :param topComp: [description], defaults to None
        :type topComp: [type], optional
        :return: [description]
        :rtype: [type]
        """
        
        r2c = leafComp.root2cam
        
        return r2c
        
    #then this
    def applyCamera(self, basicTransform: Component.BasicTransform):
        """
        method to be subclassed for  behavioral or logic computation 
        when visits Components. 
        
        In this case calculate the l2w BasicTransform component matrix
        
        """
        if (isinstance(basicTransform,Component.BasicTransform)) == False:
            return #in Python due to duck typing we need to check this!
        print(self.getClassName(), ": apply(BasicTransform) called from CameraSystem - Calc: Local2Cam")
        
        #l2world of basicTransform has been calculated by the TransformSystem before this System
        l2w = basicTransform.l2world
        r2c = self._camera.root2cam
        proj = self._camera.projMat
        l2c = l2w @ r2c @ proj
        basicTransform.update(l2cam=l2c) 
        
    #first this     
    def apply(self, cam: Component.Camera):
        """
        method to be subclassed for  behavioral or logic computation 
        when visits Camera Components. 
        
        In this case ths sole purpose is to calculate the 
        the r2c (root to camera) matrix
        
        """
        if (isinstance(cam,Component.Camera)) == False:
            return #in Python due to duck typing we need to check this!
        print(self.getClassName(), ": apply(BasicTransform) called from CameraSystem - Calc: Root2Cam")
        
        # getRoot2Cam returns the one component of the Local2Cam = Local2World * Root2Cam
        r2cam = self.getRoot2Camera(cam)
        #update root2cam of Camera
        cam.update(root2cam=r2cam)
        #save camera component if not specified on constructor
        self._camera = cam 



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
    
    
    def apply(self, renderMesh: Component.RenderMesh):
        """
        method to be subclassed for  behavioral or logic computation 
        when visits Components. 
        
        """
        print(self.getClassName(), ": apply(RenderMesh) called")
        renderMesh.update()
    
    
            
