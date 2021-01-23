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
    def get_classname(cls):
        return cls.__name__
    
    def update(self):
        """
        method to be subclassed for  behavioral or logic computation 
        when visits Components of an EntityNode. 
        
        """
        pass



class RenderGPU(System):
    """
    A basic forward rendering system based on GPU shaders
    :param System: [description]
    :type System: [type]
    """
    
    
    def dfs_update(self, graph, source):
        """ a non-recursive Depth First Search algorithm
        based on https://likegeeks.com/depth-first-search-in-python/
        
        :param graph: [the graph to traverse]
        :type graph: [dictionary]
        :param source: [the node to start searching]
        :type source: [string]
        """
        
        if source is None or source not in graph:
            return "invalid input"

        path = []
        stack = [source]

        while (len(stack) != 0):
            s = stack.pop()
            if s not in path:
                path.append(s)
            if s not in graph:
                #leaf node
                continue
            for neighbor in graph[s]:
                stack.append(neighbor)

        return ' '.join(path)
        
    def dfs_update_recursive(self, graph, source, path = []):
        """a recursive DFS update for a dictionary based simple graph

        :param graph: [description]
        :type graph: [type]
        :param source: [description]
        :type source: [type]
        :param path: [description], defaults to []
        :type path: list, optional
        """
        if source not in path:
            path.append(source)
            
            if source not in graph:
                # leaf node, backtrack
                return path
            
            for neighbor in graph[source]:
                path = self.dfs_update_recursive(graph, neighbor, path)
                
        return path
        
       
    def update(self, recursive = False, graph = None, source = None):
        if recursive is True:
            return self.dfs_update_recursive(graph, source)
        else:
            return self.dfs_update(graph, source)
            
