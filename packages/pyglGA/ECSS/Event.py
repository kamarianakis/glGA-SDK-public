""" Event classes, part of the glGA SDK ECSS
    
glGA SDK v2021.0.5 ECSS (Entity Component System in a Scenegraph)
@Coopyright 2020-2021 George Papagiannakis
    
The Event class is the mechanism for Event management in the glGA ECSS
based on the Mediator and Observer design patterns.

"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from dataclasses import dataclass

import numpy as np

import pyglGA.ECSS.utilities as util
from pyglGA.ECSS.Entity import Entity, EntityDfsIterator
from pyglGA.ECSS.Component import BasicTransform, Camera, Component
from pyglGA.ECSS.System import System, TransformSystem, CameraSystem, RenderSystem
from pyglGA.ECSS.ECSSManager import ECSSManager
from pyglGA.GUI.Viewer import SDL2Window, ImGUIDecorator, RenderWindow

@dataclass
class Event:
    """A simple dataclass that encapsulates an Event
    """
    name: str
    id: Any
    value: Any


class EventPublisher(ABC):
    """
    Interface class for all EventManagers that act as Publishers/Subjects (based on the Observer design pattern)
    or as Mediators (based on the Mediator design pattern) 
    """
    
    @abstractmethod
    def notify(self, component: Any, event: Event):
        raise NotImplementedError
    

class EventManager(EventPublisher):
    """
    Main Mediator (Subject/Publisher) class that contains list of Observers/Subscribers (Components) that is being 
    subscribed (notified) from and delegates to Systems to act upon these events invoked from these Components.
    """
    
    def __init__(self):
        self._publishers: Dict[str,Any]={}
        self._subscribers: Dict[str,Any]={}
        self._actuators: Dict[str,Any]={}
    
    def notify(self, component: Any, event: Event):
        print(f'\n{EventManager.getClassName()}: notify() reacts from {component} with {event}\n')
        
        # hardcode it for now, in a refactored version search if there is a match in the dictionaries
        # i.e. no need to hardcode this in the future:
        # just add event name and appropriate subscribers, publishers, actuators
        # and run matchmaking here between subscribers-actuators
        # all needed data are passed from the Event.value
        # and the appopriate actuator (System) will know what to do
        if event.name == "OnUpdateBackground":
            print(f'\n{event.name}: will be actuated from the appropriate system\n')
        
        
        """
        if event.name == "OnUpdateTRS":
            if comp.name == "BasicTransform":
                ts=_world.getSystem(UpdateTRS)
                comp.accept(ts, event)
        """ 
        
    '''
    @GPTODO NEED REFACTORING these methods once API is stable
    def subscribe(self, component: Any):
        self._subscribers.append(component)
        
    def unsubscribe(self, component: Any):
        self._subscribers.remove(component)
    '''
    
    @classmethod
    def getClassName(cls):
        return cls.__name__    
