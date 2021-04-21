"""
Test Event Unit tests, part of the glGA SDK ECSS
    
glGA SDK v2021.0.5 ECSS (Entity Component System in a Scenegraph)
@Coopyright 2020-2021 George Papagiannakis

"""


import unittest
import time
import numpy as np

import pyglGA.ECSS.utilities as util
from pyglGA.ECSS.System import System, TransformSystem, CameraSystem
from pyglGA.ECSS.Entity import Entity
from pyglGA.ECSS.Component import BasicTransform, Camera
from pyglGA.ECSS.Event import Event, EventManager
from pyglGA.GUI.Viewer import SDL2Window, ImGUIDecorator

class TestEvent(unittest.TestCase):
    
    def setUp(self):
        """
        setup common scene for Event testing
        """ 
        #simple RenderWindow
        self.gWindow = SDL2Window(windowTitle="RenderWindow Event Testing")
        self.gGUI = ImGUIDecorator(self.gWindow)
        #simple scenegraph
        self.gameObject = Entity("root") 
        self.gameComponent = BasicTransform()
        self.gameObject.add(self.gameComponent)
    
    def test_init(self):
        """simple tests for Event dataclass
        """
        print("TestEvent:test_init START".center(100, '-'))
        
        trsMat = util.translate(10.0,20.0,30.0)
        e = Event("OnUpdate", 100, trsMat)
        
        mT = np.array([
            [1.0,0.0,0.0,10.0],
            [0.0,1.0,0.0,20.0],
            [0.0,0.0,1.0,30.0],
            [0.0,0.0,0.0,1.0],
        ],dtype=np.float,order='F')
        
        self.assertEqual(mT.tolist(), e.value.tolist())
        self.assertEqual(e.name, "OnUpdate")
        self.assertEqual(e.id, 100)
        np.testing.assert_array_equal(e.value,mT)
        
        e.id = 101
        self.assertEqual(e.id, 101)
        
        print(e.value)
        print("\n Event e: ",e)
        
        print("TestEvent:test_init END".center(100, '-'))
    
    def test_notify(self):
        """simple Event notification from GUI
        """
        print("TestEvent:test_notify START".center(100, '-'))
        
        # instantiate new EventManager
        _eManager = EventManager()
        
        # instantiate new RenderWindow that will generate an event and set the Renderwindow._eventManager object
        
        # subscribe a RenderWindow to the EventManager
        
        # call self._eventManager.notify(self, "OnUpdateTRS") from within the RenderWindow when a GUI event is generated
        
        # how to connect the viewer that generates the Event with the appropriate component listening for that event?
        
        # 1. create a custom System that in the apply2BasicTransform() performs basic Event handling
        # 2. question is how to know which component to apply to since the Renderwindow generated that Event and not the Component?
        #   - we could also subscribe that component as an observer to the Event Manager based on that Event
        #   - essential build two data structures:
        #    - { Event: [ComponentSource, ComponentDestination]}
        #    - { Event: System }
        # ComponentDestination.accept(system)
        
        self.gGUI.init() #calls ImGUIDecorator::init()-->SDL2Window::init()
        
        running = True
        # MAIN RENDERING LOOP
        while running:
            self.gGUI.display()
            running = self.gGUI.event_input_process(running)
            self.gGUI.display_post()
        self.gGUI.shutdown()
        
        print("TestEvent:test_notify END".center(100, '-'))