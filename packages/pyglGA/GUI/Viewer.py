"""
Viewer classes, part of the pyglGA SDK ECSS
    
glGA SDK v2021.0.5 ECSS (Entity Component System in a Scenegraph)
@Copyright 2020-2021 George Papagiannakis
    
The classes below are all related to the GUI and Display part of the SDK

Basic design principles are based on the Decorator Design pattern:
	• https://refactoring.guru/design-patterns/decorator
	• https://github.com/faif/python-patterns/blob/master/patterns/structural/decorator.py
"""

from __future__         import annotations
from abc                import ABC, abstractmethod
from typing             import List
from collections.abc    import Iterable, Iterator

import sdl2
import sdl2.ext
from sdl2.keycode import SDLK_ESCAPE
from sdl2.video import SDL_WINDOWPOS_CENTERED, SDL_WINDOW_ALLOW_HIGHDPI
import OpenGL.GL as gl
from OpenGL.GL import shaders
import imgui
from imgui.integrations.sdl2 import SDL2Renderer
  
import pyglGA.ECSS.utilities as util


class RenderWindow(ABC):
    """
    The Abstract base class of the Viewer GUI/Display sub-system of pyglGA
    based on the Decorator Pattern, this class is "wrapped" by decorators
    in order to provide extra cpapabilities e.g. SDL2 window, context and ImGUI widgets    
    """     
        
    @abstractmethod
    def init(self):
        raise NotImplementedError
    
    abstractmethod
    def init_post(self):
        raise NotImplementedError
    
    @abstractmethod
    def display(self):
        raise NotImplementedError
    
    @abstractmethod
    def display_post(self):
        raise NotImplementedError
    
    @abstractmethod
    def shutdown(self):
        raise NotImplementedError
    
    @abstractmethod
    def event_input_process(self, running = True):
        raise NotImplementedError
    
    @classmethod
    def getClassName(cls):
        return cls.__name__


class SDL2Window(RenderWindow):
    """ The concrete subclass of RenderWindow for the SDL2 GUI API 

    :param RenderWindow: [description]
    :type RenderWindow: [type]
    """
    
    def __init__(self, windowWidth = None, windowHeight = None, windowTitle = None):
        """Constructor SDL2Window for basic SDL2 parameters

        :param windowWidth: [description], defaults to None
        :type windowWidth: [type], optional
        :param windowHeight: [description], defaults to None
        :type windowHeight: [type], optional
        :param windowTitle: [description], defaults to None
        :type windowTitle: [type], optional
        """
        self._gWindow = None
        self._gContext = None
        self._gVersionLabel = "None"
        
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
             
             
    @property
    def gWindow(self):
        return self._gWindow
    
    
    @property
    def gContext(self):
        return self._gContext
    
    
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
    
    
    def init_post(self):
        """
        Post init method for SDL2
        this should be ctypiically alled AFTER all other GL contexts have been created
        """
        pass
    
    
    def display(self):
        """
        Main display window method to be called standalone or from within a concrete Decorator
        """
        #GPTODO make background clear color as parameter at class level
        gl.glClearColor(0.0,0.0,0.0,1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glDisable(gl.GL_CULL_FACE)
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
        #print(f'{self.getClassName()}: display()')
    
    
    def display_post(self):
        """
        To be called at the end of each drawn frame to swap double buffers
        """
        sdl2.SDL_GL_SwapWindow(self._gWindow)
        #print(f'{self.getClassName()}: display_post()')       
    
    
    def shutdown(self):
        """
        Shutdown and cleanup SDL2 operations
        """
        print(f'{self.getClassName()}: shutdown()')
        if (self._gContext and self._gWindow is not None):
            sdl2.SDL_GL_DeleteContext(self._gContext)
            sdl2.SDL_DestroyWindow(self._gWindow)
            sdl2.SDL_Quit()   


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
        return running


class RenderDecorator(RenderWindow):
    """
    Main Decorator class that wraps a RenderWindow so that all other Decorator classes can dynamically be
    adding layered functionality on top of the wrapee (RenderWindow) e.g. ImGUI widgets etc.

    :param RenderWindow: [description]
    :type RenderWindow: [type]
    """
    def __init__(self, wrapee: RenderWindow):
        self._wrapeeWindow = wrapee
    
    
    @property
    def wrapeeWindow(self):
        return self._wrapeeWindow
    
    
    def init(self):
        """
        [summary]
        """
        self._wrapeeWindow.init()
        print(f'RenderDecorator: init()')
        
        
    def display(self):
        """
        Main decorator display method
        """
        self._wrapeeWindow.display()
        
        
    def shutdown(self):
        """
        [summary]
        """
        self._wrapeeWindow.shutdown()
        print(f'RenderDecorator: shutdown()')   
        
        
    def event_input_process(self, running = True):
        """
        extra decorator method to handle input events
        :param running: [description], defaults to True
        :type running: bool, optional
        """
        self._wrapeeWindow.event_input_process(running = True)
    
    
    def display_post(self):
        """
        Post diplay method after all other display calls have been issued
        """
        self._wrapeeWindow.display_post()
    
    
    def init_post(self):
        """
        Post init method
        this should be ctypiically alled AFTER all other GL contexts have been created, e.g. ImGUI context
        """
        self._wrapeeWindow.init_post()
                    
class ImGUIDecorator(RenderDecorator):
    """
    ImGUI decorator

    :param RenderDecorator: [description]
    :type RenderDecorator: [type]
    """
    def __init__(self, wrapee: RenderWindow, imguiContext = None):
        super().__init__(wrapee)
        if imguiContext is None:
            self._imguiContext = imgui.create_context()
        else:
            self._imguiContext = imguiContext
        self._imguiRenderer = None
    
    
    def init(self):
        """
        [summary]
        """
        self.wrapeeWindow.init()
        if self._imguiContext is None:
            print("Window could not be created! ImGUI Error: ")
            exit(1)
        else:
            print("Yay! ImGUI context created successfully")
        
        # GPTODO here is the problem: SDL2Decorator takes an SDLWindow as wrappee wheras
        # ImGUIDEcorator takes and SDL2Decorator and decorates it!
        if isinstance(self.wrapeeWindow, SDL2Window):   
            self._imguiRenderer = SDL2Renderer(self.wrapeeWindow._gWindow)
        
        print(f'{self.getClassName()}: init()')
        
        
    def display(self):
        """
        ImGUI decorator display: calls wrapee (RenderWindow::display) as well as extra ImGUI widgets
        """
        self.wrapeeWindow.display()
        #render the ImGUI widgets
        self.extra()
        #print(f'{self.getClassName()}: display()')
        
        
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
            #imgui event
            self._imguiRenderer.process_event(event)
        #imgui input
        self._imguiRenderer.process_inputs()
        return running
        
        
    def display_post(self):
        # render imgui (after 3D scene and just before the SDL double buffer swap window)
        imgui.render()
        self._imguiRenderer.render(imgui.get_draw_data())
        # call the SDL window window swapping in the end of the scene as final render action
        self.wrapeeWindow.display_post()
        
        
    def extra(self):
        """sample ImGUI widgets to be rendered on a RenderWindow
        """
        imgui.set_next_window_size(300.0, 150.0)
        
        #start new ImGUI frame context
        imgui.new_frame()
        
        #demo ImGUI window with all widgets
        imgui.show_test_window()
        #new custom imgui window
        imgui.begin("pyglGA ImGUI window", True)
        #labels inside the window
        imgui.text("PyImgui + PySDL2 integration successful!")
        imgui.text(self._wrapeeWindow._gVersionLabel)
        #end imgui frame context
        imgui.end()
        
        #print(f'{self.getClassName()}: extra()')


if __name__ == "__main__":
    # The client code.
    
    gWindow = SDL2Window()
    gWindow.init()
    gWindow.init_post()
    running = True
    # MAIN RENDERING LOOP
    while running:
        gWindow.display()
        running = gWindow.event_input_process(running)
        gWindow.display_post()
    gWindow.shutdown()