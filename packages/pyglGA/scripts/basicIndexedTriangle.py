"""
A basic triangle featuring normals VBO and indexed ones utilising Shader and VertexArray classes from pyglGA
in a standalone, manner.
    
glGA SDK v2021 ECSS (Entity Component System in a Scenegraph)
@Coopyright 2020-2021 George Papagiannakis

"""

from __future__         import annotations
from abc                import ABC, abstractmethod
from typing             import List
from collections.abc    import Iterable, Iterator
import os  
import sys
from pathlib import Path

import OpenGL.GL as gl
from OpenGL.GL import shaders
import sdl2
import sdl2.ext
from sdl2.keycode import SDLK_ESCAPE
from sdl2.video import SDL_WINDOWPOS_CENTERED, SDL_WINDOW_ALLOW_HIGHDPI
import imgui
from imgui.integrations.sdl2 import SDL2Renderer
import numpy as np

class Shader():
    """
    A concrete Shader class
    """
    
    COLOR_VERT = """#version 410
        layout (location=0) in vec4 position;
        layout (location=1) in vec4 colour;
        out vec4 theColour;
        void main()
        {
            gl_Position = position;
            theColour = colour;
        }
    """
    
    COLOR_FRAG = """#version 410
        in vec4 theColour;
        out vec4 outputColour;
        void main()
        {
            //outputColour = vec4(1, 0, 0, 1);
            outputColour = theColour;
        }
    """
    
    def __init__(self, name=None, type=None, id=None, vertex_source=None, fragment_source=None):
      
        
        self._parent = self
        
        self._glid = None
        
        if not vertex_source:
            self._vertex_source = Shader.COLOR_VERT
        else:
            self._vertex_source = vertex_source
            
        if not fragment_source:
            self._fragment_source = Shader.COLOR_FRAG
        else:
            self._fragment_source = fragment_source
        #self.init(vertex_source, fragment_source) #init Shader under a valid GL context
    
    @property
    def glid(self):
        return self._glid
    
    @property
    def vertex_source(self):
        return self._vertex_source
    
    @vertex_source.setter
    def vertex_source(self, value):
        self._vertex_source = value
    
    @property
    def fragment_source(self):
        return self._fragment_source
    
    @fragment_source.setter
    def fragment_source(self, value):
        self._fragment_source = value
    
    def __del__(self):
        gl.glUseProgram(0)
        if self._glid:
            gl.glDeleteProgram(self._glid)
    
    def disableShader(self):
        gl.glUseProgram(0)
        
    def enableShader(self):
        gl.glUseProgram(self._glid)
            
    @staticmethod
    def _compile_shader(src, shader_type):
        src = open(src, 'r').read() if os.path.exists(src) else src
        #src = src.decode('ascii') if isinstance(src, bytes) else src.decode
        shader = gl.glCreateShader(shader_type)
        gl.glShaderSource(shader, src)
        gl.glCompileShader(shader)
        status = gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS)
        src = ('%3d: %s' % (i+1, l) for i,l in enumerate(src.splitlines()) ) 
        print('Compile shader success for %s\n%s\n%s' % (shader_type, status, src))
        if not status:
            log = gl.glGetShaderInfoLog(shader).decode('ascii')
            gl.glDeleteShader(shader)
            src = '\n'.join(src)
            print('Compile failed for %s\n%s\n%s' % (shader_type, log, src))
            return None
        return shader
        
    
    def update(self):
        print("Shader: update() called")
        
     
    def init(self):
        """
        shader extra initialisation from raw strings or source file names
        """
        vert = self._compile_shader(self._vertex_source, gl.GL_VERTEX_SHADER)
        frag = self._compile_shader(self._fragment_source, gl.GL_FRAGMENT_SHADER)
        
        if vert and frag:
            self._glid = gl.glCreateProgram()
            gl.glAttachShader(self._glid, vert)
            gl.glAttachShader(self._glid, frag)
            gl.glLinkProgram(self._glid)
            gl.glDeleteShader(vert)
            gl.glDeleteShader(frag)
            status = gl.glGetProgramiv(self._glid, gl.GL_LINK_STATUS)
            if not status:
                print(gl.glGetProgramInfoLog(self._glid).decode('ascii'))
                gl.glDeleteProgram(self._glid)
                self._glid = None


class VertexArray():
    """
    A concrete VertexArray class

    """
    def __init__(self, name=None, type=None, id=None, attributes=None, index=None, primitive = gl.GL_TRIANGLES, usage=gl.GL_STATIC_DRAW):
        
        self._parent = self
        
        self._glid = None
        self._buffers = [] #store all GL buffers
        self._draw_command = None
        self._arguments = (0,0)
        self._attributes = attributes
        self._index = index
        self._usage = usage
        self._primitive = primitive #e.g. GL.GL_TRIANGLES
        #self.init(attributes, index, usage) #init after a valid GL context is active
    
    @property
    def glid(self):
        return self._glid
    
    @property
    def attributes(self):
        # vertex positions, colors, normals, texcoords lists
        return self._attributes
    
    @attributes.setter
    def attributes(self, value):
        self._attributes = value
    
    @property
    def index(self):
        return self._index
    
    @index.setter
    def index(self, value):
        self._index = value
    
    @property
    def usage(self):
        return self._usage
    
    @usage.setter
    def usage(self, value):
        self._usage = value
        
    @property
    def primitive(self):
        return self._primitive
    
    @usage.setter
    def primitive(self, value):
        self._primitive = value
    
    def __del__(self):
        gl.glDeleteVertexArrays(1, [self._glid])
        gl.glDeleteBuffers(len(self._buffers), self._buffers)
    
    def draw(self):
        # draw a vertex Array as direct array or index array
        #print("VertexArray: draw() called")
        
        gl.glBindVertexArray(self._glid)
        self._draw_command(self._primitive, *self._arguments)
        #gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)
        gl.glBindVertexArray(0)
        
    def update(self):
        #print("VertexArray: update() called")
        self.draw()
    
    def init(self):
        """
        extra method for extra initialisation pf VertexArray
        Vertex array from attributes and optional index array. 
        Vertex Attributes should be list of arrays with one row per vertex. 
        """
        # create and bind(use) a vertex array object
        self._glid = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self._glid)
        nb_primitives, size = 0, 0
        
        # load buffer per vertex attribute (in a list with index = shader layout)
        for loc, data in enumerate(self._attributes):
            if data is not None:
                # bind a new VBO, upload it to GPU, declare size and type
                self._buffers.append(gl.glGenBuffers(1))
                data = np.array(data, np.float32, copy=False)
                nb_primitives, size = data.shape
                gl.glEnableVertexAttribArray(loc)
                gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._buffers[-1])
                gl.glBufferData(gl.GL_ARRAY_BUFFER, data, self._usage)
                gl.glVertexAttribPointer(loc, size, gl.GL_FLOAT, False, 0, None)
                
        
        #optionally create and upload an index buffer for this VBO         
        self._draw_command = gl.glDrawArrays
        self._arguments = (0, nb_primitives)
        if self._index is not None:
            self._buffers += [gl.glGenBuffers(1)]
            index_buffer = np.array(self._index, np.int32, copy=False)
            gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self._buffers[-1])
            gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, index_buffer, self._usage)
            self._draw_command = gl.glDrawElements
            self._arguments = (index_buffer.size, gl.GL_UNSIGNED_INT, None)

        # cleanup and unbind so no accidental subsequent state update
        gl.glBindVertexArray(0)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)

class SDL2Window():
    """ The concrete subclass of RenderWindow for the SDL2 GUI API 

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
        print(f'SDL2Window init()')
        
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
        print(f'SDL2Window: shutdown()')
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


if __name__ == "__main__":
    # The client main code.
    
    # ------------------------------
    # vertex attribute arrays and shaders
    # ------------------------------
    vertexData = np.array([
            [0.0, 0.0, 0.0, 1.0],
            [0.5, 1.0, 0.0, 1.0],
            [1.0, 0.0, 0.0, 1.0]
        ],dtype=np.float32) 
    
    vertexData2 = np.array([
            [0.0, 0.0, 0.0, 1.0],
            [0.5, -1.0, 0.0, 1.0],
            [1.0, 0.0, 0.0, 1.0]
        ],dtype=np.float32) 
    
    colorVertexData = np.array([
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 1.0],
            [0.0, 0.0, 1.0, 1.0]
    ], dtype=np.float32)
    
    index = np.array((0,1,2), np.uint32)
    
    COLOR_VERT2 = """#version 410
        layout (location=0) in vec4 position;
        layout (location=1) in vec4 colour;
        out vec4 theColour;
        void main()
        {
            gl_Position = position;
            theColour = colour;
        }
    """
    
    COLOR_FRAG2 = """#version 410
        in vec4 theColour;
        out vec4 outputColour;
        void main()
        {
            outputColour = vec4(1, 0, 0, 1);
            //outputColour = theColour;
        }
    """
    
    # ------------------------------
    # main scene
    # ------------------------------
    
    gWindow = SDL2Window()
    gWindow.init()
    
    vArray4 = VertexArray()
    vArray5 = VertexArray()
    shaderDec4 = Shader()
    #shaderDec5 = Shader(vertex_source=COLOR_VERT2, fragment_source=COLOR_FRAG2)
    
    # ---------------------------------------
    #  reading shaders as external files
    # ---------------------------------------
    entries = Path('.')
    for entry in entries.iterdir():
        print(entry.name)
        
    with open('./scripts/color.vert', 'r') as f:
        vShader = f.read()
    with open('./scripts/color.frag', 'r') as f:
        fShader = f.read()
    shaderDec5 = Shader(vertex_source=vShader, fragment_source=fShader)
    
    attr = list()
    attr.append(vertexData)
    attr.append(colorVertexData)
    
    attr2 = list()
    attr2.append(vertexData2)
    attr2.append(colorVertexData)
    
    # init() shaderDec4, vArray4
    vArray4.attributes = attr
    vArray4.index = index
    vArray4.init()
    vArray5.attributes = attr2
    vArray5.index = index
    vArray5.init()
    shaderDec4.init()
    shaderDec5.init()
    
    running = True
    # MAIN RENDERING LOOP
    while running:
        gWindow.display()
        running = gWindow.event_input_process(running)
        # draw vArray4 with Shader4 and vArray5 with Shader5
        shaderDec4.enableShader()
        vArray4.update()
        shaderDec4.disableShader()
        shaderDec5.enableShader()
        vArray5.update()
        shaderDec5.disableShader()
        # call ImGUI render and final SDL swap window  
        gWindow.display_post()
    
    del shaderDec4
    del shaderDec5
    del vArray4
    del vArray5    
    gWindow.shutdown()