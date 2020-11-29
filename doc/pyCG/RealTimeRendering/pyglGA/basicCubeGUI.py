# This is a basicCubeGUI shader-based OpenGL example
# This notebook has been updated by Prof. George Papagiannakis as an introduction to the glGA SDK v2020.1
# based on the supervised final year BSc project of G. Evangelou, University of Crete
# Copyright 2020, University of Crete and FORTH


import ctypes
import sys
import numpy
from sdl2 import *
import sdl2.ext
import imgui as ImGui
from imgui.integrations.sdl2 import SDL2Renderer
from OpenGL.GL import *
from OpenGL.GL import shaders


#some global variables before we absorb them into classes
windowWidth     = 1024
windowHeight    = 768

# ImGUI variables
state           = False
color1          = 0., .0, .5
wireFrame       = False
f               = 0.

# OpenGL variables
NumVertices     = 36  # (6 faces)(2 triangles/face)(3 vertices/triangle)
index           = 0
shaderProgram   = None
VAO             = None
VBO             = None

# 36 x vec4
points = numpy.arange(144, dtype=numpy.float32) #36 floats *4 bytes = 144
points = points.reshape((36, 4))
points = numpy.zeros_like(points) #Return an array of zeros with the same shape and type as a given array.

# 36 x vec4
colors = numpy.arange(144, dtype=numpy.float32)
colors = colors.reshape((36, 4))
colors = numpy.zeros_like(colors)

# Vertex Positions
vertices = numpy.array([
    # Vertex Positions
    (-0.5, -0.5, 0.5, 1.0),
    (-0.5, 0.5, 0.5, 1.0),
    (0.5, 0.5, 0.5, 1.0),
    (0.5, -0.5, 0.5, 1.0),
    (-0.5, -0.5, -0.5, 1.0),
    (-0.5, 0.5, -0.5, 1.0),
    (0.5, 0.5, -0.5, 1.0),
    (0.5, -0.5, -0.5, 1.0),
], dtype=numpy.float32)

# Vertex Colours
vertex_colors = numpy.array([
    (0.0, 0.0, 0.0, 1.0),  # black
    (1.0, 0.0, 0.0, 1.0),  # red
    (1.0, 1.0, 0.0, 1.0),  # yellow
    (0.0, 1.0, 0.0, 1.0),  # green
    (0.0, 0.0, 1.0, 1.0),  # blue
    (1.0, 0.0, 1.0, 1.0),  # magenta
    (1.0, 1.0, 1.0, 1.0),  # white
    (0.0, 1.0, 1.0, 1.0),  # cyan
], dtype=numpy.float32)

TranslationMat = numpy.array([
    (1.0, 0.0, 0.0, 0.0),
    (0.0, 1.0, 0.0, 0.0),
    (0.0, 0.0, 1.0, 0.0),
    (-0.5, 0.0, 0.0, 1.0),
], dtype=numpy.float32)

def quad(a, b, c, d):
    """create a quad out of four coordinates

    Args:
        a ([int]): [index to first vertex]
        b ([int]): [index to second vertex]
        c ([int]): [index to third vertex]
        d ([int]): [index to fourth vertex]
    """
    global index
    global colors
    global points
    global vertex_colors
    global vertices

    colors[index] = vertex_colors[a]
    points[index] = vertices[a]
    index += 1
    colors[index] = vertex_colors[b]
    points[index] = vertices[b]
    index += 1
    colors[index] = vertex_colors[c]
    points[index] = vertices[c]
    index += 1

    colors[index] = vertex_colors[a]
    points[index] = vertices[a]
    index += 1
    colors[index] = vertex_colors[c]
    points[index] = vertices[c]
    index += 1
    colors[index] = vertex_colors[d]
    points[index] = vertices[d]
    index += 1

def init():
    """ 
    Initialises an SDL2 window with an OpenGL state context

    Parameters:
    None

    Returns:
        gWindow: the SDL2 window
        gContext: the OpenGL context of the gWindow
        gVersionLabel: the OpeGL Version and context info
    """

    if SDL_Init(SDL_INIT_VIDEO | SDL_INIT_TIMER) != 0:
        print("SDL could not initialize! SDL Error: ", SDL_GetError())
        raise RuntimeError('SDL could not initialize!')
        exit(1)

    print("\nYay! Initialized SDL successfully in basicCubeGUI!")
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_FLAGS, SDL_GL_CONTEXT_FORWARD_COMPATIBLE_FLAG)
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_PROFILE_MASK, SDL_GL_CONTEXT_PROFILE_CORE)
    SDL_GL_SetAttribute(SDL_GL_DOUBLEBUFFER, 1)
    SDL_GL_SetAttribute(SDL_GL_DEPTH_SIZE, 24)
    SDL_GL_SetAttribute(SDL_GL_STENCIL_SIZE, 8)
    SDL_GL_SetAttribute(SDL_GL_ACCELERATED_VISUAL, 1)
    SDL_GL_SetAttribute(SDL_GL_MULTISAMPLEBUFFERS, 1)
    SDL_GL_SetAttribute(SDL_GL_MULTISAMPLESAMPLES, 16)
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MAJOR_VERSION, 4) # OpenGL 4.1 version
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MINOR_VERSION, 1)
    
    SDL_SetHint(SDL_HINT_MAC_CTRL_CLICK_EMULATE_RIGHT_CLICK, b"1")
    #SDL_SetHint(SDL_HINT_VIDEO_HIGHDPI_DISABLED, b"1")

    # CREATE WINDOW
    window_title = 'BasicCubeGUI'
    windowWidth = 1024
    windowHeight = 768
    gWindow = SDL_CreateWindow(window_title.encode(), SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,windowWidth, windowHeight, SDL_WINDOW_OPENGL )

    if gWindow is None:
        print("Window could not be created! SDL Error: ", SDL_GetError())
        raise RuntimeError('Failed to create SDL window')
        #exit(1)

    print("Yay! Created window successfully in basicCubeGUI!")
    gContext = SDL_GL_CreateContext(gWindow)
    print("Yay! Created OpenGL context successfully in basicCubeGUI!\n\n")
    
    if gContext is None:
        print("OpenGL context could not be created! SDL Error: ", SDL_GetError())
        raise RuntimeError('OpenGL context could not be created!')

    SDL_GL_MakeCurrent(gWindow, gContext)

    if SDL_GL_SetSwapInterval(1) < 0:
        print("Warning: Unable to set VSync! SDL Error: " + SDL_GetError())
        raise RuntimeError('Unable to set VSync! SDL Error:!')

    gVersionLabel = 'OpenGL +', glGetString(GL_VERSION).decode() + ', GLSL', glGetString(GL_SHADING_LANGUAGE_VERSION).decode() + ', Renderer', glGetString(GL_RENDERER).decode()
    print(gVersionLabel)

    return gWindow, gContext, str(gVersionLabel)


def initCube():
    """
    initialises basic vertex, fragment shaders in order to display a  basic colored Cube with orthographic projection
    """
    
    # we want to access the three global variables for the shaders
    global  shaderProgram
    global  VAO
    global  VBO
    global TranslationMat
    global points
    
    #first we generate and then bind a VAO on the client GPU side that will contain the VBOs for the triangle
    VAO = glGenVertexArrays(1) #id is 1
    glBindVertexArray(VAO) #use, open VAO here
    
    # build up the 6 basic cube faces
    quad(1, 0, 3, 2)
    quad(2, 3, 7, 6)
    quad(3, 0, 4, 7)
    quad(6, 5, 1, 2)
    quad(4, 5, 6, 7)
    quad(5, 4, 0, 1)

    print(TranslationMat)
    print("--------------------------------------")
    # print(vertices)
    # points = numpy.dot(points, TranslationMat)
    print(points)
    
    vertexShader = shaders.compileShader("""
    #version 410
    layout (location=0) in vec4 vPosition;
    layout (location=1) in vec4 vColor;
    out vec4 color;

    uniform mat4 translate;

    void main()
    {
        // uncomment to witness the effect of translation to the left on X by -0.5
        gl_Position = translate * vPosition;

        // uncomment to have the cube centered on 0.0.0
        //gl_Position =  vPosition;

        color = vColor;
        // debug
        // if(translate[0][0]==-0.5) color=vec4(0.0,1.0,0.0,1.0);
    }
    """, GL_VERTEX_SHADER)

    fragmentShader = shaders.compileShader("""
    #version 410
    in vec4 color;
    out vec4 outputColour;
    void main()
    {
        outputColour = color;
        //outputColour = vec4(0.0,1.0,0.0,1.0);
    }
    """, GL_FRAGMENT_SHADER)
    
    #build the shaderProgram our of the two shaders
    shaderProgram = shaders.compileProgram(vertexShader, fragmentShader)
    
    # active shader program
    glUseProgram(shaderProgram)
    
    # Create vertices VBO on server side GPU
    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, points.nbytes + colors.nbytes, None, GL_STATIC_DRAW)
    glBufferSubData(GL_ARRAY_BUFFER, 0, points.nbytes, points)
    glBufferSubData(GL_ARRAY_BUFFER, points.nbytes, colors.nbytes, colors)

    # enable array and set up data
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 0, None)

    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(points.nbytes))

    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 1.0)

    global TranslateMat
    TranslateMat = glGetUniformLocation(shaderProgram, "translate")
    # glUniformMatrix4fv(TranslateMat, 1, GL_FALSE,  TranslationMat)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    # Only one VAO can be bound at a time, so disable it to avoid altering it accidentally
    glBindVertexArray(0)
    
    return shaderProgram, VAO, VBO # for unit test purposes


def displayCube():
    """
    Uses the previously created shader program, binds the VAO on the client side and renders the cube using triangles
    """
    global shaderProgram
    global VAO
    global wireFrame
    global TranslationMat
    
    #glClearColor(0, 0, 0.3, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glDisable(GL_CULL_FACE)
    
    # active shader program
    #glUseProgram(shaderProgram)

    if wireFrame:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    try:
        glBindVertexArray(VAO)
        glUniformMatrix4fv(TranslateMat, 1, GL_FALSE, TranslationMat)
        # glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
        # draw cube
        glDrawArrays(GL_TRIANGLES, 0, NumVertices)
    finally:
        glBindVertexArray(0)
        # glUseProgram(0)

def displayGUI():
    """
        displays the ImGUI window to control the background color and the 'wireframe' rendering of the cube
    """
    
    global wireFrame
    global color1
    global state
    global f
    # imgui.new_frame()
    ImGui.set_next_window_size(400.0, 160.0)
    #imgui.set_next_window_position(10., 0.)
    ImGui.begin("BasicCube GUI", True)

    # Shows Simple text
    ImGui.text("Hello, CG world!")

    # Goes to a new line
    ImGui.new_line()

    # Creates a simple slider
    changed, f = ImGui.slider_float("float", f, 0.0, 1.0)
    ImGui.separator()

    # Manipulates colors
    changed, color1 = ImGui.color_edit3("clear color", *color1)
    ImGui.separator()

    # Creates a checkbox
    changed, checkbox = ImGui.checkbox("Wireframe", state)
    if changed:
        if checkbox is False:
            wireFrame = False
            state = False
        if checkbox is True:
            wireFrame = True
            state = True
    
    #strFrameRate = str(("Application average" , 1000.0/float(ImGui.get_io().framerate), "ms/frame (", str(ImGui.get_io().framerate)," FPS)"))
    strFrameRate = str(("Application average: ", ImGui.get_io().framerate, " FPS"))
    ImGui.text(strFrameRate)

    ImGui.end()


def main():
    """
    The main method that after calling init() it starts the main rendering loop.
    This loop re-draws a shader-based Cube, the ImGUI sample window in immediate mode and finally swaps the SDL2 double buffer windows
    """
    global wireFrame
    
    gWindow, gContext, gVersionLabel = init()
    
    # Enable depth test
    glEnable(GL_DEPTH_TEST)
    # Accept fragment if it closer to the camera than the former one
    glDepthFunc(GL_LESS)
    # Setup GL shaders, data, etc.
    initCube()
    
    #ImGui.create_default_context(purpose=Purpose.SERVER_AUTH, cafile=None, capath=None, cadata=None)
    imguiContext = ImGui.create_context()
    
    if imguiContext is None:
        print("Window could not be created! ImGUI Error: ")
        exit(1)
    else:
        print("Yay! ImGUI context created successfully")
        
    renderer = SDL2Renderer(gWindow)
    
    running = True
    # MAIN LOOP
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == SDL_KEYDOWN:
                if event.key.keysym.sym == SDLK_ESCAPE:
                    running = False
                if event.key.keysym.sym == SDLK_w:
                    if wireFrame == False:
                        wireFrame = True
                    else:
                        wireFrame = False
            if event.type == SDL_QUIT:
                running = False
            renderer.process_event(event)
        renderer.process_inputs()

        glClearColor(*color1, 1.)
        glClear(GL_COLOR_BUFFER_BIT)

         #render the shader-based cube in each frame, before any ImGUI widget
        displayCube()
        
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
     

        ImGui.set_next_window_size(300.0, 150.0)
        # start new frame context
        ImGui.new_frame()
        
        displayGUI()
        
        # open new window context
        ImGui.begin("Our first window!", True)
        # draw text label inside of current window
        ImGui.text("PyImgui + PySDL2 integration successful!")
        ImGui.text(gVersionLabel)
        # close current window context
        ImGui.end()
        
        # pass all ImGUI drawing commands to the rendering pipeline
        # and close ImGUI frame context
        ImGui.render() #always draw last ImGUI
        renderer.render(ImGui.get_draw_data())

        SDL_GL_SwapWindow(gWindow)
    # CLOSING
    renderer.shutdown()
    SDL_GL_DeleteContext(gContext)
    SDL_DestroyWindow(gWindow)
    SDL_Quit()


if __name__ == "__main__":
    main()





