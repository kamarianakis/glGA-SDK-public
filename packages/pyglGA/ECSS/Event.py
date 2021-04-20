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
from pyglGA.GUI.Viewer import SDL2Window, ImGUIDecorator

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
    def notify(self, component: Component, event: Event):
        raise NotImplementedError
    

class EventManager(EventPublisher):
    """
    Main Mediator (Subject/Publisher) class that contains list of Observers/Subscribers (Components) that is being 
    subscribed (notified) from and delegates to Systems to act upon these events invoked from these Components.
    """
    
    def __init__(self):
        self._subscribers: List[Component]=[]
    
    def notify(self, component: Component, event: Event):
        print(f'\n{EventManager.getClassName()}: notify() reacts from {component} with {event}\n')
    
    def subscribe(self, component: Component):
        self._subscribers.append(component)
        
    def unsubscribe(self, component: Component):
        self._subscribers.remove(component)
    
    @classmethod
    def getClassName(cls):
        return cls.__name__    
