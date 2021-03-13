"""
BasicWindow example, showcasing the pyglGA SDK ECSS
    
glGA SDK v2021.0.5 ECSS (Entity Component System in a Scenegraph)
@Coopyright 2020-2021 George Papagiannakis
    
The classes below are all related to the GUI and Display of 3D 
content using the OpenGL, GLSL and SDL2, ImGUI APIs, on top of the
pyglGA ECSS package
"""

from __future__         import annotations
import numpy as np

from pyglGA.GUI.Viewer import SDL2Decorator, SDL2Window, ImGUIDecorator


def main():
    gWindow = SDL2Window()
    gContext = SDL2Decorator(gWindow)
    #gGUI = ImGUIDecorator(gContext)
    
    gContext.init()
    gContext.init_post()
    
    # MAIN RENDERING LOOP
    running = True
    while running:
        gContext.display()
        running = gContext.event_input_process(running)
        gContext.display_post()
    gContext.shutdown()


if __name__ == "__main__":
    main()