
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

shaderProgram   = None
VAO             = None
VBO             = None

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

    print("\nYay! Initialized SDL successfully in basicTriangle!")
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
    SDL_SetHint(SDL_HINT_VIDEO_HIGHDPI_DISABLED, b"1")

    # CREATE WINDOW
    window_title = 'BasicTriangle'
    windowWidth = 1024
    windowHeight = 768
    gWindow = SDL_CreateWindow(window_title.encode(), SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,windowWidth, windowHeight, SDL_WINDOW_OPENGL)

    if gWindow is None:
        print("Window could not be created! SDL Error: ", SDL_GetError())
        raise RuntimeError('Failed to create SDL window')
        #exit(1)

    print("Yay! Created window successfully in basicTriangle!")
    gContext = SDL_GL_CreateContext(gWindow)
    print("Yay! Created OpenGL context successfully in basicTriangle!\n\n")
    
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


def initTriangle():
    """
    initialises basic vertex, fragment shaders in order to display a 2D basic Triangle with orthographic projection
    """
    
    # we want to access the three global variables for the shaders
    global  shaderProgram
    global  VAO
    global  VBO
    
    #first we generate and then bind a VAO on the client GPU side that will contain the VBOs for the triangle
    VAO = glGenVertexArrays(1) #id is 1
    glBindVertexArray(VAO) #use, open VAO here
    
    vertexShader = shaders.compileShader("""
        #version 410
        layout (location=0) in vec4 position;
        layout (location=1) in vec4 colour;
        out vec4 theColour;
        void main()
        {
            gl_Position = position;
            theColour = colour;
        }
        """, GL_VERTEX_SHADER)
    
    fragmentShader = shaders.compileShader("""
        #version 410
        in vec4 theColour;
        out vec4 outputColour;
        void main()
        {
            outputColour = theColour;
        }
        """, GL_FRAGMENT_SHADER)
    
    #build the shaderProgram our of the two shaders
    shaderProgram = shaders.compileProgram(vertexShader, fragmentShader)
    
    # create the basic vertex array containing both vertex positions as well as vertex colours
    
    vertexData = numpy.array(
        [
            #vertex positions
            0.0, 0.0, 0.0, 1.0,
            0.5, 1.0, 0.0, 1.0,
            1.0, 0.0, 0.0, 1.0,
            
            #vertex colours
            1.0, 0.0, 0.0, 1.0,
            0.0, 1.0, 0.0, 1.0,
            0.0, 0.0, 1.0, 1.0,
        ],dtype=numpy.float32
    )
    
    #create the VBO on the server memory of the GPU
    VBO = glGenBuffers(1) #id is 1
    glBindBuffer(GL_ARRAY_BUFFER, VBO) # use, open VBO here
    glBufferData(GL_ARRAY_BUFFER, vertexData.nbytes, vertexData, GL_STATIC_DRAW)
    #enable strides vertex array for both positions (first) and colours (subsequently, after first bytes)
    glEnableVertexAttribArray(0) #id is 0
    glVertexAttribPointer(0,4,GL_FLOAT, GL_FALSE, 0, None) #how to fill in the vertex array
    #second colours array
    glEnableVertexAttribArray(1) #id is 1
    glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(48)) #float32 is 4 bytes, 12 floats as vertices * 4 = 48 bytes
    
    glBindBuffer(GL_ARRAY_BUFFER,0) #close VBO here
    # Only one VAO can be bound at a time, so disable it to avoid altering it accidentally
    glBindVertexArray(0) # close VAO
    
    print("Yay! Created shaderProgram, VAO and VBO in basicTriangle!\n\n")
    return shaderProgram, VAO, VBO


def displayTriangle():
    """
    Uses the previously created shader program, binds the VAO on the client side and draws using triangles
    """
    global shaderProgram
    global VAO
    glClearColor(0, 0, 0.3, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # active shader program
    glUseProgram(shaderProgram)

    try:
        glBindVertexArray(VAO)
        # glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
        # draw triangle
        glDrawArrays(GL_TRIANGLES, 0, 3)
    finally:
        glBindVertexArray(0)
        glUseProgram(0)


def main():
    """
    The main method that after calling init() it starts the main rendering loop.
    This loop re-draws an ImGUI sample window in immediate mode and swaps the SDL2 double buffer windows
    """
    
    gWindow, gContext, gVersionLabel = init()
    #ImGui.create_default_context(purpose=Purpose.SERVER_AUTH, cafile=None, capath=None, cadata=None)
    imguiContext = ImGui.create_context()
    
    if imguiContext is None:
        print("Window could not be created! ImGUI Error: ")
        exit(1)
    else:
        print("Yay! ImGUI context created successfully")
        
    renderer = SDL2Renderer(gWindow)
    
    # Enable depth test
    glEnable(GL_DEPTH_TEST)
    # Accept fragment if it closer to the camera than the former one
    glDepthFunc(GL_LESS)
    # Setup GL shaders, data, etc.
    initTriangle()

    running = True
    # MAIN LOOP
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == SDL_KEYDOWN:
                if event.key.keysym.sym == SDLK_ESCAPE:
                    running = False
            if event.type == SDL_QUIT:
                running = False
            renderer.process_event(event)
        renderer.process_inputs()

        glClearColor(0.0, 0.0, 0.0, 1)
        glClear(GL_COLOR_BUFFER_BIT)

        ImGui.set_next_window_size(300.0, 150.0)
        # start new frame context
        ImGui.new_frame()
        # open new window context
        ImGui.begin("Our first window!", True)
        # draw text label inside of current window
        ImGui.text("PyImgui + PySDL2 integration successful!")
        ImGui.text(gVersionLabel)
        # close current window context
        ImGui.end()
        
        #render the shader-based triangle in each frame, before any ImGUI widget
        displayTriangle()
        
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





