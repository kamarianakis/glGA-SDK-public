
import ctypes
import sys
import numpy
from sdl2 import *
import sdl2.ext
import imgui as ImGui
from imgui.integrations.sdl2 import SDL2Renderer
from OpenGL.GL import *
from OpenGL.GL import shaders


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
        exit(1)

    print("\nYay! Initialized SDL successfully!")
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
    window_title = 'BasicWindow'
    windowWidth = 1024
    windowHeight = 768
    gWindow = SDL_CreateWindow(window_title.encode(), SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,windowWidth, windowHeight, SDL_WINDOW_OPENGL)

    if gWindow is None:
        print("Window could not be created! SDL Error: ", SDL_GetError())
        raise RuntimeError('Failed to create SDL window')
        #exit(1)

    print("Yay! Created window successfully!")
    gContext = SDL_GL_CreateContext(gWindow)
    print("Yay! Created OpenGL context successfully!\n\n")
    
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
        
        #a sample imGUI window with all widgets
        ImGui.show_test_window()
        
        # open new window context
        ImGui.begin("Our first window!", True)
        # draw text label inside of current window
        ImGui.text("PyImgui + PySDL2 integration successful!")
        ImGui.text(gVersionLabel)
        # close current window context
        ImGui.end()
        # pass all drawing commands to the rendering pipeline
        # and close frame context
        ImGui.render()
        renderer.render(ImGui.get_draw_data())

        SDL_GL_SwapWindow(gWindow)
    # CLOSING
    renderer.shutdown()
    SDL_GL_DeleteContext(gContext)
    SDL_DestroyWindow(gWindow)
    SDL_Quit()


if __name__ == "__main__":
    main()





