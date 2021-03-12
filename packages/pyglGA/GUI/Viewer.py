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
from sdl2.events import SDL_KEYDOWN
import sdl2.ext


import pyglGA.ECSS.System
import uuid  
import pyglGA.ECSS.utilities as util
from sdl2.keycode import SDLK_ESCAPE
from sdl2.video import SDL_WINDOWPOS_CENTERED, SDL_WINDOW_ALLOW_HIGHDPI
import OpenGL.GL as gl
from OpenGL.GL import shaders

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
        
        #extra SDL2 members    
        self._gVersionLabel = "none"
        self._gRenderer = None
            
    
    def init(self):
        """
        Initialise an SDL2 RenderWindow, not directly but via the SDL2Decorator
        """
        print(f'{self.getClassName()}: init()')
        
        #SDL_Init for the window initialization
        sdl_not_initialised = sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO | sdl2.SDL_INIT_TIMER)
        if sdl_not_initialised !=0:
            print("SDL2 could not be initialised! SDL Error: ", sdl2.SDL_GetError())
            exit(1)
        
        #setting OpenGL attributes for the GL state and context 4.1
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_FLAGS,
                                 sdl2.SDL_GL_CONTEXT_FORWARD_COMPATIBLE_FLAG
                                 )
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_PROFILE_MASK,
                                 sdl2.SDL_GL_CONTEXT_PROFILE_CORE
                                 )
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_DOUBLEBUFFER, 1)
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_DEPTH_SIZE, 24)
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_STENCIL_SIZE, 8)
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_ACCELERATED_VISUAL, 1)
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_MULTISAMPLEBUFFERS, 1)
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_MULTISAMPLESAMPLES, 16)
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MAJOR_VERSION, 4)
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MINOR_VERSION, 1)
        sdl2.SDL_SetHint(sdl2.SDL_HINT_MAC_CTRL_CLICK_EMULATE_RIGHT_CLICK, b"1")
        sdl2.SDL_SetHint(sdl2.SDL_HINT_VIDEO_HIGHDPI_DISABLED, b"1")
        
        #creating the SDL2 window
        self._gWindow = sdl2.SDL_CreateWindow(self._windowTitle.encode(), 
                                              sdl2.SDL_WINDOWPOS_CENTERED,
                                              sdl2.SDL_WINDOWPOS_CENTERED,
                                              self._windowWidth,
                                              self._windowHeight,
                                              sdl2.SDL_WINDOW_ALLOW_HIGHDPI)
        if self._gWindow is None:
            print("Window could not be created! SDL Error: ", sdl2.SDL_GetError())
            exit(1)
            
        #create the OpenGL context for rendering into the SDL2Window that was constructed just before
        self._gContext = sdl2.SDL_GL_CreateContext(self._gWindow)
        if self._gContext is None:
            print("OpenGL Context could not be created! SDL Error: ", sdl2.SDL_GetError())
            exit(1)
        sdl2.SDL_GL_MakeCurrent(self._gWindow, self._gContext)
        if sdl2.SDL_GL_SetSwapInterval(1) < 0:
            print("Warning: Unable to set VSync! SDL Error: " + sdl2.SDL_GetError())
            exit(1)
        #obtain the GL versioning system info
        self._gVersionLabel = f'OpenGL {gl.glGetString(gl.GL_VERSION).decode()} GLSL {gl.glGetString(gl.GL_SHADING_LANGUAGE_VERSION).decode()} Renderer {gl.glGetString(gl.GL_RENDERER).decode()}'
        print(self._gVersionLabel)
    
    
    
    def display(self):
        """
        [summary]
        """
        #GPTODO make background clear color as parameter at class level
        gl.glClearColor(0.0,0.0,0.0,1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        
        print(f'{self.getClassName()}: display()')
        
    
    
    def shutdown(self):
        """
        Shutdown and cleanup SDL2 operations
        """
        print(f'{self.getClassName()}: shutdown()')
        if (self._gRenderer and self._gContext and self._gWindow is not None):
            self._gRenderer.shutdown()
            sdl2.SDL_GL_DeleteContext(self._gContext)
            sdl2.SDL_DestroyWindow(self._gWindow)
            sdl2.SDL_QUIT()   


class RenderDecorator(RenderWindow):
    """

    :param RenderWindow: [description]
    :type RenderWindow: [type]
    """
    
    def __init__(self, wrapee: RenderWindow):
        self._wrapeeWindow = wrapee
    
    def init(self):
        """
        [summary]
        """
        self._wrapeeWindow.init()
        print(f'RenderDecorator: init()')
        
    def display(self):
        """
        [summary]
        """
        self._wrapeeWindow.display()
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
    
    def init_post(self):
        """
        Post init method for SDL2
        this should be ctypiically alled AFTER all other GL contexts have been created, e.g. ImGUI context
        """
        #self._wrapeeWindow._gRenderer = sdl2.SDL2Renderer(self._wrapeeWindow._gWindow)
        
    def display(self):
        """
        [summary]
        """
        super().display()
        #self.extra()
        print(f'{self.getClassName()}: display()')
        
    def display_post(self):
        """
        To be called at the end of each drawn frame to swap double buffers
        """
        
        sdl2.SDL_GL_SwapWindow(self._wrapeeWindow._gWindow)
        print(f'{self.getClassName()}: display_post()')    
        
    def extra(self):
        """[summary]
        """
        print(f'{self.getClassName()}: extra()')
    
    def event_input_process(self, running = True):
        """
        process SDL2 basic events and input
        """
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                    running = False
            if event.type == sdl2.SDL_QUIT:
                running = False
            self._wrapeeWindow._gRenderer.process_event(event)
        self._wrapeeWindow._gRenderer.process_inputs()
        

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
    #gGUI = ImGUIDecorator(gContext)
    
    #gGUI.init() # calls gContext.init() as well as ImGUI init stuff
    # in a rendering while loop
        #gGui.display() # calls gContext.display()
    
    running = True
        # MAIN RENDERING LOOP
    while running:
        gContext.display()
        gContext.event_input_process(running)
        gContext.display_post()
    gContext.shutdown()