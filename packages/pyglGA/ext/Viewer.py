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
        raise NotImplementedError
    
    @abstractmethod
    def display(self):
        raise NotImplementedError
    
    @abstractmethod
    def shutdown(self):
        raise NotImplementedError
    
    @classmethod
    def getClassName(cls):
        return cls.__name__


class SDL2Window(RenderWindow):
    """[summary]

    :param RenderWindow: [description]
    :type RenderWindow: [type]
    """
    
    def __init__(self):
        pass
    
    def init(self):
        """
        [summary]
        """
        print(f'{self.getClassName()}: init()')
        
    def display(self):
        """
        [summary]
        """
        print(f'{self.getClassName()}: display()')
        
    
    def shutdown(self):
        """
        [summary]
        """
        print(f'{self.getClassName()}: shutdown()')   


class RenderDecorator(RenderWindow):
    """

    :param RenderWindow: [description]
    :type RenderWindow: [type]
    """
    
    def __init__(self, wrapee: RenderWindow):
        self._wrapee = wrapee
    
    def init(self):
        """
        [summary]
        """
        self._wrapee.init()
        print(f'{self.getClassName()}: init()')
        
    def display(self):
        """
        [summary]
        """
        self._wrapee.display()
        print(f'{self.getClassName()}: display()')
        
    def shutdown(self):
        """
        [summary]
        """
        print(f'{self.getClassName()}: shutdown()')   

class SDL2Decorator(RenderDecorator):
    """

    :param RenderDecorator: [description]
    :type RenderDecorator: [type]
    """
    
    def init(self):
        """
        [summary]
        """
        super().init()
        print(f'{self.getClassName()}: init()')
        
    def display(self):
        """
        [summary]
        """
        super().display()
        self.extra()
        print(f'{self.getClassName()}: display()')
        
    def extra(self):
        """[summary]
        """
        print(f'{self.getClassName()}: extra()')
        

class ImGUIDecorator(RenderDecorator):
    """
    

    :param RenderDecorator: [description]
    :type RenderDecorator: [type]
    """
    def init(self):
        """
        [summary]
        """
        super().init()
        print(f'{self.getClassName()}: init()')
        
    def display(self):
        """
        [summary]
        """
        self.extra()
        super().display()
        print(f'{self.getClassName()}: display()')
        
    def extra(self):
        """[summary]
        """
        print(f'{self.getClassName()}: extra()')


if __name__ == "__main__":
    # The client code.
    
    gWindow = SDL2Window()
    gContext = SDL2Decorator(gWindow)
    gGUI = ImGUIDecorator(gContext)
    
    gGUI.init() # calls gContext.init() as well as ImGUI init stuff
    # in a rendering while loop
        #gGui.display() # calls gContext.display()