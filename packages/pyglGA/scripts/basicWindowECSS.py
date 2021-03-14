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

from pyglGA.GUI.Viewer import SDL2Window, ImGUIDecorator


def main():
    gWindow = SDL2Window()
    #gGUI = ImGUIDecorator(gContext)
    
    gWindow.init()
    gWindow.init_post()
    
    # MAIN RENDERING LOOP
    running = True
    while running:
        gWindow.display()
        running = gWindow.event_input_process(running)
        gWindow.display_post()
    gWindow.shutdown()


if __name__ == "__main__":
    main()