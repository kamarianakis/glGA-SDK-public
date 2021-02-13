"""
Test System Unit tests, part of the glGA SDK ECS
    
glGA SDK v2020.1 ECS (Entity Component System)
@Coopyright 2020-2021 George Papagiannakis

"""


import unittest
from System import *


class TestSystem(unittest.TestCase):
    def test_init(self):
        """
        default constructor of System class
        """
        print("\TestSystem:test_init() START")
        
        #mySystem = System(100, "baseSystem", "abstract")
        mySystem = System()
        mySystem.name = "baseSystem"
        mySystem.type = "abstract"
        mySystem.id = 100
        
        self.assertEqual(mySystem.name, "baseSystem")
        self.assertEqual(mySystem.type,"abstract")
        self.assertEqual(mySystem.id, 100)
        
        print("TestSystem:test_init() END")
        
    
class TestTransformSystem(unittest.TestCase):
    
    def test_getLocal2World(self):
        """
        System test_getLocal2World() test
        """
        print("TestTransformSystem:test_getLocal2World() START")
        gameObject = Entity("root", "Entity", "0")
        gameObject1 = Entity("node1", "Entity", "1")
        gameObject2 = Entity("node2", "Entity", "2")
        gameObject3 = Entity("node3", "Entity", "3")
        
        trans4 = BasicTransform("trans4", "BasicTransform", "7")
        trans5 = BasicTransform("trans5", "BasicTransform", "8")
        trans6 = BasicTransform("trans6", "BasicTransform", "9")
        transRoot = BasicTransform("transRoot", "BasicTransform", "0")
        
        myComponent = BasicTransform("myComponent", "BasicTransform", "100")
        mT = np.array([
            [1.0,0.0,0.0,1.0],
            [0.0,1.0,0.0,2.0],
            [0.0,0.0,1.0,3.0],
            [0.0,0.0,0.0,1.0],
        ],dtype=np.float,order='F')
        
        mT2 = np.array([
            [1.0,0.0,0.0,2.0],
            [0.0,1.0,0.0,3.0],
            [0.0,0.0,1.0,4.0],
            [0.0,0.0,0.0,1.0],
        ],dtype=np.float,order='F')
        
        mTf = np.array([
            [1.0,0.0,0.0,3.0],
            [0.0,1.0,0.0,5.0],
            [0.0,0.0,1.0,7.0],
            [0.0,0.0,0.0,1.0],
        ],dtype=np.float,order='F')
        
        myComponent.l2world = mT
        
        trans4.trs = translate(1.0, 2.0, 3.0)
        trans6.trs = translate(2.0, 3.0, 4.0)
        gameObject.add(gameObject1)
        gameObject.add(transRoot)
        gameObject1.add(gameObject2)
        gameObject2.add(gameObject3)
        gameObject1.add(trans6)
        gameObject2.add(trans4)
        gameObject3.add(trans5)
        
        """
        root
            |
            node1, transRoot
            |   
            node2, trans6: translate(2,3,4)
                |       
                node3,  trans4: translate(1,2,3)
                    |
                    trans5
        """
        self.assertEqual(trans4, gameObject2.getChildByType("BasicTransform"))
        self.assertEqual(gameObject3, gameObject2.getChildByType("Entity"))
        self.assertIn(gameObject1, gameObject._children)
        self.assertEqual(gameObject2.getNumberOfChildren(), 2)
        
         #instantiate a new TransformSystem System to visit all scenegraph componets
        transUpdate = TransformSystem("transUpdate", "TransformSystem", "001")
        trans5.accept(transUpdate)
        #check if the local2World was correctly calculated upstream
        print(trans5.l2world)
        print(mT @ mT2)
        np.testing.assert_array_equal(mTf,trans5.l2world)
        
        #reapplhy the TransformSystem this time to another BasicTransform
        # to calculate its l2world
        trans6.accept(transUpdate)
        print(trans6.l2world)
        print(mT2)
        np.testing.assert_array_equal(mT2,trans6.l2world)
        
        print("TestTransformSystem:test_getLocal2World() END")
        
    def test_TransformSystem_use(self):
        """
        TransformSystem() use case test
        """
        print("TestTransformSySystem() START")
        gameObject = Entity("root", "Group", "1")
        gameObject2 = Entity("node2", "Group", "2")
        gameObject3 = Entity("node3", "Group", "3")
        gameObject4 = Entity("node4", "Group", "4")
        gameObject5 = Entity("node5", "Group", "5")
        gameObject6 = Entity("node6", "Group", "6")
        gameObject7 = Entity("node7", "Group", "7")
        trans4 = BasicTransform("trans4", "Transform", "7")
        trans5 = BasicTransform("trans5", "Transform", "8")
        trans6 = BasicTransform("trans6", "Transform", "9")
        gameObject.add(gameObject2)
        gameObject.add(gameObject4)
        gameObject.add(gameObject7)
        gameObject2.add(gameObject3)
        gameObject2.add(gameObject5)
        gameObject3.add(gameObject6)
        gameObject4.add(trans4)
        gameObject5.add(trans5)
        gameObject6.add(trans6)
        
        self.assertIn(gameObject2, gameObject._children)
        self.assertIn(gameObject4, gameObject._children)
        self.assertIn(trans4, gameObject4._children)
        self.assertIn(gameObject3, gameObject2._children)
        self.assertIn(trans5, gameObject5._children)
        
        #test the EntityDfsIterator to traverse the above ECS scenegraph
        dfsIterator = iter(gameObject)
        print(gameObject)
        
        #instantiate a new TransformSystem System to visit all scenegraph componets
        transUpdate = TransformSystem("transUpdate", "TransformSystem", "001")
        
        nodePath = []
        done_traversing = False
        while(not done_traversing):
            try:
                traversedComp = next(dfsIterator)
            except StopIteration:
                print("\n-------- end of Scene reached, traversed all Components!")
                done_traversing = True
            else:
                if (traversedComp is not None): #only if we reached end of Entity's children traversedComp is None
                    print(traversedComp)
                    
                    #accept a TransformSystem visitor System for each Component that can accept it (BasicTransform)
                    traversedComp.accept(transUpdate) #calls specific concrete Visitor's apply(), which calls specific concrete Component's update
                    #nodePath.append(traversedComp) #no need for this now
        #print("".join(str(nodePath)))
        
        print("TestTransformSySystem() END")
        

class TestCameraSystem(unittest.TestCase):
    
    def test_CameraSystem_use(self):
        """
        TestCameraSystem() use case test
        """
        print("test_CameraSystem_use() START")
        gameObject = Entity("root", "Group", "1")
        gameObject2 = Entity("node2", "Group", "2")
        gameObject3 = Entity("node3", "Group", "3")
        gameObject4 = Entity("node4", "Group", "4")
        gameObject5 = Entity("node5", "Group", "5")
        gameObject6 = Entity("node6", "Group", "6")
        gameObject7 = Entity("node7", "Group", "7")
        trans4 = BasicTransform("trans4", "Transform", "7")
        trans5 = BasicTransform("trans5", "Transform", "8")
        trans6 = BasicTransform("trans6", "Transform", "9")
        gameObject.add(gameObject2)
        gameObject.add(gameObject4)
        gameObject.add(gameObject7)
        gameObject2.add(gameObject3)
        gameObject2.add(gameObject5)
        gameObject3.add(gameObject6)
        gameObject4.add(trans4)
        gameObject5.add(trans5)
        gameObject6.add(trans6)
        
        self.assertIn(gameObject2, gameObject._children)
        self.assertIn(gameObject4, gameObject._children)
        self.assertIn(trans4, gameObject4._children)
        self.assertIn(gameObject3, gameObject2._children)
        self.assertIn(trans5, gameObject5._children)
        
        #test the EntityDfsIterator to traverse the above ECS scenegraph
        dfsIterator = iter(gameObject)
        print(gameObject)
        
        #instantiate a new TransformSystem System to visit all scenegraph componets
        transUpdate = TransformSystem("transUpdate", "TransformSystem", "001")
        camUpdate = CameraSystem("camUpdate", "CameraUpdate", "200")
        
        nodePath = []
        done_traversing = False
        while(not done_traversing):
            try:
                traversedComp = next(dfsIterator)
            except StopIteration:
                print("\n-------- end of Scene reached, traversed all Components!")
                done_traversing = True
            else:
                if (traversedComp is not None): #only if we reached end of Entity's children traversedComp is None
                    print(traversedComp)
                    
                    #accept a TransformSystem visitor System for each Component that can accept it (BasicTransform)
                    traversedComp.accept(transUpdate) #calls specific concrete Visitor's apply(), which calls specific concrete Component's update
                    #nodePath.append(traversedComp) #no need for this now
        #print("".join(str(nodePath)))
        
        print("test_CameraSystem_use() END")

class TestRenderSystem(unittest.TestCase):
    def test_init(self):
        """
        default constructor of System class
        """
        print("\TestRenderSystem:test_init() START")
        
        #mySystem = System(100, "baseSystem", "abstract")
        mySystem = RenderSystem()
        mySystem.name = "RenderSystem"
        mySystem.type = "System"
        mySystem.id = 101
        
        self.assertEqual(mySystem.name, "RenderSystem")
        self.assertEqual(mySystem.type,"System")
        self.assertEqual(mySystem.id, 101)
        
        print("TestRenderSystem:test_init() END")
    
    def test_update(self):
        """
        test_update of System Depth First Search traversal
        based on https://likegeeks.com/depth-first-search-in-python/
        """
        print("\TestSystem:test_update() START")
        
        #mySystem = System(100, "baseSystem", "abstract")
        mySystem = RenderSystem()
        mySystem.name = "mySystem"
        mySystem.type = "Rendering"
        mySystem.id = 102
        
        self.assertEqual(mySystem.name, "mySystem")
        self.assertEqual(mySystem.type,"Rendering")
        self.assertEqual(mySystem.id, 102)
        
        print("TestSystem:test_update() END")
        

if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=3, exit=False)