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
import pyglGA.ECSS.utilities as util
from pyglGA.ECSS.Entity import Entity
from pyglGA.ECSS.Component import BasicTransform, Camera, RenderMesh
from pyglGA.ECSS.System import System, TransformSystem, CameraSystem, RenderSystem
from pyglGA.ext.Scene import Scene
from pyglGA.ECSS.ECSSManager import ECSSManager


def main(imguiFlag = False):
    s1 = Scene()
    scene = Scene()    
    
    # Scenegraph with Entities, Components
    rootEntity =scene.world.createEntity(Entity(name="RooT"))
    entityCam1 =scene.world.createEntity(Entity(name="entityCam1"))
    scene.world.addEntityChild(rootEntity,entityCam1)
    trans1 =scene.world.addComponent(entityCam1, BasicTransform(name="trans1", trs=util.translate(1.0,2.0,3.0)))
        
    entityCam2 =scene.world.createEntity(Entity(name="entityCam2"))
    scene.world.addEntityChild(entityCam1,entityCam2)
    trans2 =scene.world.addComponent(entityCam2, BasicTransform(name="trans2", trs=util.translate(2.0,3.0,4.0)))
    orthoCam =scene.world.addComponent(entityCam2, Camera(util.ortho(-100.0, 100.0, -100.0, 100.0, 1.0, 100.0), "orthoCam","Camera","500"))
        
    node4 =scene.world.createEntity(Entity(name="node4"))
    scene.world.addEntityChild(rootEntity,node4)
    trans4 =scene.world.addComponent(node4, BasicTransform(name="trans4"))
    mesh1 =scene.world.addComponent(node4, RenderMesh(name="mesh1"))
        
    # Systems
    transUpdate =scene.world.createSystem(TransformSystem("transUpdate", "TransformSystem", "001"))
    camUpdate =scene.world.createSystem(CameraSystem("camUpdate", "CameraUpdate", "200"))
    renderUpdate =scene.world.createSystem(RenderSystem("renderUpdate", "RenderUpdate", "300",orthoCam))

    gWindow = SDL2Window()
    gGUI = ImGUIDecorator(gWindow)
    
    if imguiFlag is True:
        gContext = gGUI
    else:
        gContext = gWindow
    
    gContext.init()
    gContext.init_post()
    
    scene.world.print()
    
    # MAIN RENDERING LOOP
    running = True
    while running:
        gContext.display()
        running = gContext.event_input_process(running)
        
        # 1. L2W traversal
        scene.world.traverse_visit(transUpdate, scene.world.root) 
        # 2. pre-camera Mr2c traversal
        scene.world.traverse_visit_pre_camera(camUpdate, orthoCam)
        # 3. run proper Ml2c traversal
        scene.world.traverse_visit(camUpdate, scene.world.root)
        # 4. run proper render traversal
        scene.world.traverse_visit(renderUpdate, scene.world.root)
        
        gContext.display_post()
    gContext.shutdown()


if __name__ == "__main__":    
    main(imguiFlag = True)