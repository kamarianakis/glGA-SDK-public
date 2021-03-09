"""
Viewer classes, part of the pyglGA SDK ECSS
    
glGA SDK v2021.0.5 ECSS (Entity Component System in a Scenegraph)
@Coopyright 2020-2021 George Papagiannakis
    
The classes below are all related to the GUI and Display part of the SDK
"""

from __future__         import annotations
from abc                import ABC, abstractmethod
from typing             import List
from collections.abc    import Iterable, Iterator

import pyglGA.ECSS.System
import uuid  
import pyglGA.ECSS.utilities as util


class RenderWindow(ABC):
    """
    The Abstract base class of the Viewer GUI/Display sub-system of pyglGA
    based on the Decorator Pattern, this class is "wrapped" by decorators
    in order to provide extra cpapabilities e.g. SDL2 window, context and ImGUI widgets    
    """
    def __init__(self):
        pass
        
    @abstractmethod
    def init(self):
        pass
    
    @abstractmethod
    def display(self):
        pass
    
    @abstractmethod
    def shutdown(self):
        pass

class SDL2Window(RenderWindow):
    pass

class RenderDecorator(RenderWindow):
    pass

class SDL2Decorator(RenderDecorator):
    pass


class ImGuiDecorator(RenderDecorator):
    pass


if __name__ == "__main__":
    # The client code.
    
    # gWindow = SDL2Window()
    # gContext = SDL2Decorator(gWindow)
    # gGUI = ImGuiDecorator(gContext)
    
    # gGui.init() # calls gContext.init() as well as ImGUI init stuff
    # in a rendering while loop
        #gGui.display() # calls gContext.display()