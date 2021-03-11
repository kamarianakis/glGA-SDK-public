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

import sdl2
import sdl2.ext


import pyglGA.ECSS.System
import uuid  
import pyglGA.ECSS.utilities as util
from sdl2.video import SDL_WINDOWPOS_CENTERED, SDL_WINDOW_ALLOW_HIGHDPI


class RenderWindow(ABC):
    """
    The Abstract base class of the Viewer GUI/Display sub-system of pyglGA
    based on the Decorator Pattern, this class is "wrapped" by decorators
    in order to provide extra cpapabilities e.g. SDL2 window, context and ImGUI widgets    
    """
    def __init__(self, gWindow = None, gContext = None):
        if gWindow is not None:
            self._gWindow = gWindow
            
        if gContext is not None:
            self._gContext = gContext
        
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
    
    def __init__(self, gWindow = None, gContext = None, windowWidth = None, windowHeight = None, windowTitle = None):
        """[summary]

        :param gWindow: [description], defaults to None
        :type gWindow: [type], optional
        :param gContext: [description], defaults to None
        :type gContext: [type], optional
        :param windowWidth: [description], defaults to None
        :type windowWidth: [type], optional
        :param windowHeight: [description], defaults to None
        :type windowHeight: [type], optional
        :param windowTitle: [description], defaults to None
        :type windowTitle: [type], optional
        """
        super().__init__()
        if windowWidth is None:
            self._windowWidth = 1024
        else:
            self._windowWidth = windowWidth
        
        if windowHeight is None:
            self._windowHeight = 768
        else:
            self._windowHeight = windowHeight
            
        if windowTitle is None:
            self._windowTitle = "SDL2Window"
        else:
            self._windowTitle = windowTitle
            
    
    def init(self):
        """
        Initialise an SDL2 RenderWindow
        """
        print(f'{self.getClassName()}: init()')
        
        sdl_initialised = sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO | sdl2.SDL_INIT_TIMER)
        if sdl_initialised !=0:
            print("SDL2 could not be initialised! SDL Error: ", sdl2.SDL_GetError())
            exit(1)
        
        self._gWindow = sdl2.SDL_CreateWindow(self._windowTitle.encode(), 
                                              sdl2.SDL_WINDOWPOS_CENTERED,
                                              sdl2.SDL_WINDOWPOS_CENTERED,
                                              self._windowWidth,
                                              self._windowHeight,
                                              sdl2.SDL_WINDOW_ALLOW_HIGHDPI)
        
        if self._gWindow is None:
            print("Window could not be created! SDL Error: ", sdl2.SDL_GetError())
            exit(1)
        
        
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
        print(f'RenderDecorator: init()')
        
    def display(self):
        """
        [summary]
        """
        self._wrapee.display()
        print(f'RenderDecorator: display()')
        
    def shutdown(self):
        """
        [summary]
        """
        print(f'RenderDecorator: shutdown()')   

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