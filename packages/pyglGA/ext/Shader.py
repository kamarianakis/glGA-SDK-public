"""
Shader classes, extension of the glGA SDK ECSS
    
glGA SDK v2021 ECSS (Entity Component System in a Scenegraph)
@Coopyright 2020-2021 George Papagiannakis
    
The Shader Compoment class is the dedicated to a specific type of data container in the pyglGA ECSS
that of assembling, using and destroying OpenGL API shader programs

Based on the Composite and Iterator design patterns:
	• https://refactoring.guru/design-patterns/composite
    • https://github.com/faif/python-patterns/blob/master/patterns/structural/composite.py
    • https://refactoring.guru/design-patterns/iterator
    • https://github.com/faif/python-patterns/blob/master/patterns/behavioral/iterator.py


"""

from __future__         import annotations
from abc                import ABC, abstractmethod
from typing             import List
from collections.abc    import Iterable, Iterator
import os  
import sys

import OpenGL.GL as gl
from OpenGL.GL import shaders

from pyglGA.ECSS.System import System, RenderSystem, SystemDecorator
from pyglGA.ECSS.Component import Component, BasicTransform, Camera, ComponentDecorator, RenderMesh, CompNullIterator, BasicTransformDecorator
import uuid  
import pyglGA.ECSS.utilities as util
from pyglGA.ext.VertexArray import VertexArray

class Shader(Component):
    """
    A concrete Shader class

    :param Component: [description]
    :type Component: [type]
    """
    
    COLOR_VERT = """#version 410 core
    layout(location = 0) in vec3 position;

    void main() {
        gl_Position = vec4(position, 1);
    }"""
    
    COLOR_FRAG = """#version 410 core
    out vec4 outColor;

    void main() {
        outColor = vec4(1, 0, 0, 1);
    }"""
    
    def __init__(self, name=None, type=None, id=None, vertex_source=None, fragment_source=None):
        super().__init__(name, type, id)
        
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
        print(self.getClassName(), ": update() called")
        
   
    def accept(self, system: System):
        """
        Accepts a class object to operate on the Component, based on the Visitor pattern.

        :param system: [a System object]
        :type system: [System]
        """
        system.apply2Shader(self)
    
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
    
    def __iter__(self) ->CompNullIterator:
        """ A component does not have children to iterate, thus a NULL iterator
        """
        return CompNullIterator(self) 
    
    
class ShaderGLDecorator(ComponentDecorator):
    """A decorator of the Shader Compoment to decorate it with custom standard pass-through 
    shader attributes

    :param ComponentDecorator: [description]
    :type ComponentDecorator: [type]
    """
    def init(self):
        self.component.init()
    
    def update(self):
        self.component.update()
        # add here custom shader draw calls, e.g. glGetUniformLocation(), glUniformMatrix4fv() etc.add()
        # e.g.  loc = GL.glGetUniformLocation(shid, 'projection')
        #       GL.glUniformMatrix4fv(loc, 1, True, projection)

    def disableShader(self):
        self.component.disableShader()
        
    def get_glid(self):
        return self.component.glid


class InitGLShaderSystem(System):
    """Initialise outside of the rendering loop RenderMesh, Shader, VertexArray, ShaderGLDecorator classes

    """
    def init(self):
        pass
    
    def update(self):
        """
        """
        #add here custom Shader render calls
    
        
    def apply2RenderMesh(self, renderMesh:RenderMesh):
        """
        method to be subclassed for  behavioral or logic computation 
        when visits Components.
        
        """
        print(f'\n{renderMesh} accessed within {self.getClassName()}::apply2RenderMesh() \n')
        self.update()
        
    def apply2VertexArray(self, vertexArray:VertexArray):
        """
        method to be subclassed for  behavioral or logic computation 
        when visits Components.
        
        """
        print(f'\n{vertexArray} accessed within {self.getClassName()}::apply2RenderMesh() \n')
        # Access parent Entity's RenderMesh
        parentEntity = vertexArray.parent
        parentRenderMesh = parentEntity.getChildByType(RenderMesh.getClassName())
        if parentRenderMesh:
            # Copy RenderMesh::vertex_attributes to vertexArray
            vertexArray.attributes = parentRenderMesh.vertex_attributes
            vertexArray.init()
        else:
            print("\n no RenderMesh to copy vertex attributes from! \n")
        # Init vertexArray
        
    def apply2Shader(self, shader:Shader):
        """
        method to be subclassed for  behavioral or logic computation 
        when visits Components.
        
        """
        # if there is no ShaderGLDecorator, init Shader
        # for the moment assume that the user will not be directly adding both a shader and shaderDecorator at scenegraph level
        # we can prevent this at ECSSManager level, but not at scenegraph direct access level
        shader.init()
        print(f'\n{shader} accessed within {self.getClassName()}::apply2Shader() \n')
    
    def apply2ShaderGLDecorator(self, shaderGLDecorator:ShaderGLDecorator):
        """
        method to be subclassed for  behavioral or logic computation 
        when visits Components.
        
        """
        #init ShaderGLDecorator if there is such a node
        shaderGLDecorator.init()
        print(f'\n{shaderGLDecorator} accessed within {self.getClassName()}::apply2ShaderGLDecorator() \n')


class RenderGLShaderSystem(System):
    """A decorated RenderSystem specifically for GL vertex and fragment Shaders and associated 
    VertexArray components attached to a specific Entity

    """
    def init(self):
        pass
        
    def apply2VertexArray(self, vertexArray:VertexArray):
        """
        Main GPU rendering is initiated when a vertexArray node is encountered and if a Shader/Shaderdecorator 
        and RenderMesh components are present 

        method to be subclassed for  behavioral or logic computation 
        when visits RenderMesh Components of the parent EntityNode. 
        Separate SystemDecorator is needed for each case, e.g. for rendering with GL 
        vertex and fragment Shaders: RenderShaderSystem
        
        Actuall RenderShaderSystem rendering is initiated in this update call, according to following pseudocode:
        """
        parentEntity = vertexArray.parent
        compRenderMesh = parentEntity.getChildByType(RenderMesh.getClassName())
        compShader = parentEntity.getChildByType(Shader.getClassName())
        if not compShader:
            compShader = parentEntity.getChildByType(ShaderGLDecorator.getClassName())
        
        if (vertexArray and compRenderMesh and compShader):
            self.render(vertexArray, compRenderMesh, compShader)
    
    
    def render(self, vertexArray:VertexArray = None, compRenderMesh:RenderMesh = None, compShader=None):
        """
        - Shader-based main draw():
            - retrive ShaderDecorator glid
            - useShaderProgram(ShaderDecorator.glid)
            - call ShaderDecorator::update to pass on uniform shader parameters to GPU
            - renderMeshVertexArray.execute(gl.GL_TRIANGLES)
            - userShaderProgram(0) #clean GL state
        """
        #retrieve Shader GL id
        if isinstance(compShader, Shader):
            gl.glUseProgram(compShader.glid)
        else:
            gl.glUseProgram(compShader.get_glid())
        #add here custom Shader render calls
        
        #call main draw from VertexArray
        vertexArray.update()
        
        compShader.disableShader()
        print(f'\nMain shader GL render within {self.getClassName()}::update() \n')