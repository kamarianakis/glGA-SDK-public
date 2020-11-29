# This is a basicCharacterApp shader-based OpenGL example
# This notebook has been updated by Prof. George Papagiannakis as an introduction to the glGA SDK v2020.1
# based on the supervised final year BSc project of G. Evangelou, University of Crete
# Copyright 2020, University of Crete and FORTH


import ctypes
import math
import sys
import numpy
from sdl2 import *
import sdl2.ext
import imgui as ImGui
import glm
import pyassimp
import pyassimp.postprocess
import logging
logging.basicConfig(level=logging.INFO)

from imgui.integrations.sdl2 import SDL2Renderer
from OpenGL.GL import *
from OpenGL.GL import shaders

# select which of the two pipelines for a MeshStatic or MeshDynamic (rigged, animated)
# e.g. initMeshStatic()->loadModelAssimp()->(staticMesh shaders)->displayMeshStatic()
# or the equivalent ot the above in MeshDynamic
USE_MESH_DYNAMIC = False
USE_MESH_STATIC = True

scene = None
pMesh = None

if USE_MESH_STATIC:
    fileNameS = "/Users/Giwrgakis/MyProjects/glGA-SDK/doc/pyCG/RealTimeRendering/pyglGA/models/duck.dae"
    #fileNameS = "/Users/Giwrgakis/MyProjects/glGA-SDK/doc/pyCG/RealTimeRendering/pyglGA/models/testScene.dae"
    #fileNameS = "./models/testScene.dae"
    print('Model path:',fileNameS)
    positionS = glm.vec3(100.0, 0, 0)
    rotationS = glm.vec3(0, 0, 0)
    scaleS = 10.
    
if USE_MESH_DYNAMIC:
    fileNameD = './models/astroBoy_walk3.dae'
    print('Model path :', fileNameD)
    positionD = glm.vec3(0., 0., 0.)
    rotationD = glm.vec3(0., 0., 0.)
    scaleD = 10.
    pRigMesh = None
    m_RigBuffers = None
    m_boneLocation = None
    m_pScene2 = None
    MAX_BONES = 100

# some global variables before we absorb them into classes
gWindow = None
gContext = None
windowWidth     = 1024
windowHeight    = 768
globalFPS = 0.0
my_Quat = None
Screen_FBO = None
depthrenderbuffer = None
direction = glm.vec3(-1.3, -6.6, -30.0)
position = glm.vec3(-0.08, 5, -0.9) + direction * 0.2
view_matrix = glm.lookAt(position, direction, glm.vec3(0, 2, 0))
projection_matrix = glm.perspective(90.0, 1.0 * windowWidth / windowHeight, 0.1, 80000.0)
bgColor = (1.0, 1.0, 1.0, 1.0)
currentTime = 0.
lastTime = 0.
deltaTime = 0.

#  FPS Camera 
xpos = ypos = 0
horizontalAngle = verticalAngle = 0
move_x1 = move_x2 = move_y1 = move_y2 = move_z1 = move_z2 = 0
camx1 = camx2 = camy1 = camy2 = camz1 = camz2 = 0
move_x = move_y = move_z = 100
right = glm.vec3(math.sin(horizontalAngle - 3.14 / 2.0), 0, math.cos(horizontalAngle - 3.14 / 2.0));
enable_move = 1
# Initial Field of View
rightCamVec = up = glm.vec3(0., 0., 0.)
initViewerPosition = True
# 

# Further global vars - definitely need to abstact them with classes
color4 = None
point4 = None
Index1 = 0
IndexGround = 0
NumVertices = 36
program = programPlane = programAxes = ModelView = Projection = ModelViewPlane = View = None
ProjectionPlane = LightPosition = None
vaoPlane = m_VAO = mRig_VAO = m_Buffers = programRigMesh = None
bufferPlane = 0
textureSampler = 0
vPosition = vTexCoord = vColor = vNormal = None
speed = 0.
wire = 0
cameraView = False
g_Zoom = 300.0
g_ZoomX = 0.0
g_ZoomY = 50.0
g_quat = [0., 0., 0.]
g_dir = [0., 0., -1., 0.]
viewer_pos = glm.vec3(0., 0., 0.)
viewer_dir = glm.vec3(0., 0., 0.)
viewer_up = glm.vec3(0., 1., 0.)
quatRot = None
quatToMat = None
model_view = model_viewPlane = view_mat = None
nav_mat = None
projection = None
light_position = None
showMat = True
g_resetView = False
g_useGAinterp = False
g_GAfactorDenominator = 2.0

# transforms related
initialEuler = glm.vec3(0.0,0.0,0.0)
finalRotation = glm.mat4(1.0)
angle1 = angle2 = angle3 = 0
Transforms = None
programMesh = ModelViewMesh = ProjectionMesh = ModelViewMesh1 = ProjectionMesh1 = None
vPositionMesh = vTexCoordMesh = vColorMesh = vNormalMesh = vBoneWeightMesh = vBoneIDMesh = None
LightPositionMesh = None
vaoMesh = None
model_viewMesh = None
startTime = 0

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



def GLMTests():
    """
    test glm vec, mat and quat data structures
    """
    t = glm.vec4(10., -5., 6.1, 1.)
    t0 = t1 = t2 = t3 = None
    origin = glm.vec4(0., 0., 0., 1.)
    point = glm.vec4(1., 2., 3., 1.)
    axisRaw = glm.quat(10., 1., 1., 1.)
    axis = glm.normalize(axisRaw)
    q1 = glm.quat(1., 1., 1., 1.)
    q2 = glm.quat(1.0, glm.vec3(1., 0., 0.))
    transMat = glm.mat4(1.0)
    rotMat = glm.mat4(1.0)
    mat1 = glm.mat4(1., 0., 0., 0.,
                    0., 1., 0., 0.,
                    0., 0., 1., 0.,
                    -10., 10., 10., 1.)
    # access translation vector, column major matrix
    print(mat1)
    print('x:',mat1[3, 0])
    print('y:', mat1[3, 1])
    print('z:', mat1[3, 2])

    # each row is a column
    # so we write it as a Transpose here
    mat2 = glm.mat4(glm.vec4(1., 0., 0., 10.),
                    glm.vec4(0., 1., 0., 10.),
                    glm.vec4(0., 0., 1., 10.),
                    glm.vec4(0., 0., 0., 1.))  # wrongly specified as row major

    identity = glm.mat4(1.0)

    print("\n identity mat4: \n", identity)
    print("\n transMat mat4: \n", transMat)
    print("\n rotMat mat4: \n", rotMat)
    print("\n t : \n", t)
    print("\n point : \n", point)
    print("\n mat1 mat4: \n", mat1)
    print("\n mat2 mat4: \n", mat2)
    print("\n axis : \n", axis)
    print("\n q2 : \n", q2)

    t0 = mat1[0]
    t1 = mat1[1]
    t2 = mat1[2]
    t3 = mat1[3]
    elem03 = mat1[3][0]
    print('t0, t1, t2, t3')
    print('elem03: ', elem03)

    print('t to_string: ', t)
    print('mat1 to_string: ', mat1)

    q1 = glm.conjugate(axis)
    print("conjugate-axis", q1)
    q1 = glm.inverse(axis)
    print("inverse-axis", q1)
    qMat = glm.mat4(1.0)
    qMat = glm.mat4_cast(axis)
    print("axis: q -> Mat", qMat)
    q = glm.quat_cast(qMat)
    print("q: mat -> quat", q)
    q2 = glm.rotate(q, 90., glm.vec3(1., 0., 0.))
    print("rotated q by 90 in X: ", q2)
    gInt0 = gInt = gInt1 = glm.quat(1., 1., 1., 1.)
    gInt0 = glm.slerp(q, q2, 0.)
    gInt = glm.slerp(q, q2, 0.5)
    gInt1 = glm.slerp(q, q2, 1.)
    print("interpolated gInt: [q to q2 by 0.5:", gInt)
    print("interpolated gInt: [q to q2 by 0.0:", gInt0)
    print("interpolated gInt: [q to q2 by 1.0:", gInt1)

    print('************ POINT QUATERNION INTERPOLATION EXPERIMENT **************')
    p = glm.quat(0., 0., 1., 1.)
    Q = glm.angleAxis(90., glm.vec3(0., 1., 0.))
    angle = glm.angle(Q)
    axisOfRotation = glm.axis(Q)
    print('verified quat Q angle is:', angle, 'and axis:', axisOfRotation)
    Q1 = glm.conjugate(Q)
    p2 = Q * p * Q1
    print("rotated P by 90 Y degrees:", p2)
    qIntExp = glm.slerp(p, p2, 0.5)
    print("interpolated gIntExp: [p to p2 by 0.5:", qIntExp)
    print('********* END POINT QUATERNION INTERPOLATION EXPERIMENT **********')

    transMat = glm.translate(glm.mat4(1.0), glm.vec3(10.,20.,30.))
    print("transMat", transMat)
    print(transMat)
    print('x:', transMat[3, 0])
    print('y:', transMat[3, 1])
    print('z:', transMat[3, 2])

    t = t * point
    t = transMat * glm.vec4(1.0)
    origin = mat1 * origin
    print("transMat", transMat)
    print("t", t)
    print("origin", origin)
    origin = mat2 * glm.vec4(0.0, 0.0, 0.0, 1.0)
    print("origin", origin)
    origin = glm.transpose(mat2) * glm.vec4(0., 0., 0., 1.)
    print("origin", origin)
    invMat = glm.mat4(1.0)
    invMat = glm.inverse(mat1)
    print("invMat", invMat)
    Rotate = glm.vec3(1., 1., 1.)
    Translate = glm.vec3(1., 1., 1.)
    ViewTranslate = glm.translate(glm.mat4(1.0), Translate)
    ViewRotateX = glm.rotate(ViewTranslate, Rotate.y, glm.vec3(-1., 0., 0.))

    print('origin.x: ', origin.x)

    print('*********************   Dual Quaternion tests *********************')
    print("NOT SUPPORTED IN pyGLM (YET)!")

    print('*********************   END OF GLM TESTS  *********************')

def loadModelAssimp(filepath):
    """
    Loads an assimp supported model as an assimp scene and extract vertices, normals and texcoords
    
    Args:
        filepath ([string]): [the relative path of the 3D asset]
    """
    global scene
    global pMesh
    
    print("\n loadModelAssimp() ready to load: ", filepath)
    #with pyassimp.load(filepath) as scene:
    scene = pyassimp.load(filepath)
    #scene = load(filepath)
    assert len(scene.meshes), "pyAssimp could not load mesh!"
    #assert len(scene.meshes)
    pMesh = scene.meshes[0]
    assert len(pMesh.vertices)
    
    numpy.set_printoptions(suppress=True)
    
    vertices = numpy.array(pMesh.vertices, 'f')
    normals = numpy.array(pMesh.normals, 'f')
    texCoords = numpy.array(pMesh.texturecoords[0], 'f')
    texCoords = numpy.delete(texCoords, numpy.s_[2], 1)
    """
    if texCoords == None:
        print("no texCoords on file", filepath)
    if vertices == None:
        print("no vertices on file", filepath)
    if normals == None:
        print("no normals on file", filepath)
    """
    
    print(vertices)
    print(normals)
    print(texCoords)
    
    return vertices, normals, texCoords


def initMeshStatic(filepath):
    """
        initialises the static mesh, calls loadModelAssimp, initialises shaders
    """
    global m_VAO
    global m_Buffers
    global programMesh
    
    global scene
    global pMesh
    
    global light_position
    global ModelViewMesh
    global ProjectionMesh
    global LightPositionMesh
    global textureSampler
    
    global positionS
    global rotationS
    global scaleS

    m_VAO = glGenVertexArrays(1)
    glBindVertexArray(m_VAO)
    
    # static mesh vertex and fragment shaders with Phong shading and lighting    
    meshStaticVert = shaders.compileShader("""
    #version 150 core
    #extension GL_ARB_explicit_attrib_location : enable


    layout (location=0) in vec3    vPosition;
    //in      vec4    vColor;
    layout (location=1) in vec3    vNormal;
    layout (location=2) in vec2    vTexCoord;

    out     vec4    color;
    out     vec2    texCoord;

    uniform mat4    ModelView;
    uniform mat4    Projection;
    uniform vec4    AmbientProduct, DiffuseProduct, SpecularProduct;
    uniform vec4    LightPosition;
    uniform float   Shininess;
    uniform mat4    initialTransform;


    void    main()
    {
    
        // Transform vertex position into eye coordinates
        vec3    pos = (ModelView * vec4(vPosition.x,vPosition.y,vPosition.z,1.0)).xyz;
        // calculate L in light space from Light position - vertex position (eye space)
        vec3    L = normalize(LightPosition.xyz - pos);
        // assume constant viewer at 0,0,0 (in eye space)
        vec3    E = normalize(0-pos);
        // calculate half angle vector
        vec3    H = normalize((L+E)/2);
    
        // for the rest of our Phong calculations we will need the Normal into eye space as well
        // only correct if there is no scale in MV, otherwise we use the InverseTranspose of MV
        vec3    N = normalize( ModelView*vec4(vNormal, 0.0) ).xyz;
    
        // compute terms in the illumination equation
        vec4    ambientTerm = AmbientProduct;
    
        // compute diffuse Phong Term 
        float   diffuseDotProduct = max( dot(L,N), 0.0 ); //calculate >0 only +ve values
        vec4    diffuseTerm = diffuseDotProduct * DiffuseProduct;
    
        // compute specular Phong Term
        float   specularDotProduct = pow( max(dot(N,H), 0.0), Shininess);
        vec4    specularTerm = specularDotProduct * SpecularProduct;
    
        //special provision for dark side highlights
        if (dot(L,N) < 0.0) {
        
           specularTerm = vec4(0.0,0.0,0.0,1.0);
        }
        // outpout per-vertex position in Clip space
        vec4 pos4 = vec4(vPosition.x,vPosition.y,vPosition.z,1.0);
    
        gl_Position = Projection * ModelView * initialTransform * pos4;
    
        // output lighted via the Phong algorithm each vertex color
        //color       = (ambientTerm + diffuseTerm + specularTerm) * vColor;
        color       = (ambientTerm + diffuseTerm + specularTerm);
        // pass to fragment shader per-vertex tex coords
        texCoord    = vTexCoord;
    
        }
                """, GL_VERTEX_SHADER)

    meshStaticFrag = shaders.compileShader("""
       
        #version 150 core

        //varying  vec4  color;
        in      vec4    color;
        in      vec2    texCoord;

        uniform sampler2D   TextureSampler2D;
        uniform float       TexturesPresent;

        out     vec4    colorOUT;

            void main() 
{ 
    //gl_FragColor = color* texture2D(texture, texCoord);
    //colorOUT = color * texture(TextureSampler2D, texCoord);
    //colorOUT = color;
    if (TexturesPresent>0) {
        colorOUT = color * texture(TextureSampler2D, texCoord);
    }
    else
        colorOUT = color;
        //colorOUT = vec4(0.0,0.0,1.0,1.0);
    
    //colorOUT = vec4(0.0,0.0,1.0,1.0);
    //colorOUT = color * texture(TextureSampler2D, texCoord);
} 

                """, GL_FRAGMENT_SHADER)
        
    programMesh = shaders.compileProgram(meshStaticVert, meshStaticFrag)
    glUseProgram(programMesh)
    
    pos, norm, texc = loadModelAssimp(filepath)
    
    # create the VBO
    m_Buffers = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, m_Buffers)
    glBufferData(GL_ARRAY_BUFFER, pos.nbytes + norm.nbytes + texc.nbytes, None, GL_STATIC_DRAW)
    glBufferSubData(GL_ARRAY_BUFFER, 0, pos.nbytes, pos)
    glBufferSubData(GL_ARRAY_BUFFER, pos.nbytes, norm.nbytes, norm)
    glBufferSubData(GL_ARRAY_BUFFER, pos.nbytes + norm.nbytes, texc.nbytes, texc)

    # Position (Vertex VBO)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))

    # print("Normals: ", pos)
    # Normals (Normal VBO)
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(pos.nbytes))

    # Texture (TEXCOORD VBO)
    glEnableVertexAttribArray(2)
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(pos.nbytes + norm.nbytes))

    glBindBuffer(GL_ARRAY_BUFFER, 0)

    # Index VBO
    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, pMesh.faces.nbytes, pMesh.faces, GL_STATIC_DRAW)

    light_position = glm.vec4(0., 0., -1., 0.)
    light_ambient = glm.vec4(0.2, 0.2, 0.2, 1.0)
    light_diffuse = glm.vec4(1., 1., 1., 1.)
    light_specular = glm.vec4(1., 1., 1., 1.)

    material_ambient = glm.vec4(0.5, 0.5, 0.5, 1.0)
    material_diffuse = glm.vec4(1., 1., 1., 1.)
    material_specular = glm.vec4(1., 1., 1., 1.)
    material_shininess = 100.

    ambient_product = light_ambient * material_ambient
    diffuse_product = light_diffuse * material_diffuse
    specular_product = light_specular * material_specular

    # print(ambient_product)
    # print(diffuse_product)
    # print(specular_product)

    # Checking if textures are present
    material_texture = 1
    print("Number of textures present: ", len(texc[0]))
    if len(texc[0]) <= 2:
        material_texture = 0
        print("No Textures")

    glUniform4fv(glGetUniformLocation(programMesh, "AmbientProduct"), 1, glm.value_ptr(ambient_product))
    glUniform4fv(glGetUniformLocation(programMesh, "DiffuseProduct"), 1, glm.value_ptr(diffuse_product))
    glUniform4fv(glGetUniformLocation(programMesh, "SpecularProduct"), 1, glm.value_ptr(specular_product))
    glUniform1f(glGetUniformLocation(programMesh, "Shininess"), material_shininess)
    glUniform1f(glGetUniformLocation(programMesh, "TexturesPresent"), material_texture)

     # transformation uniform
    ModelViewMesh = glGetUniformLocation(programMesh, "ModelView")
    ProjectionMesh = glGetUniformLocation(programMesh, "Projection")
    LightPositionMesh = glGetUniformLocation(programMesh, "LightPosition")

    tr = glm.translate(glm.mat4(), positionS)
    rotateX = glm.rotate(tr, rotationS.x, glm.vec3(1., 0., 0.))
    rotateY = glm.rotate(rotateX, rotationS.y, glm.vec3(0., 1., 0.))
    rotateZ = glm.rotate(rotateY, rotationS.z, glm.vec3(0., 0., 1.))
    initialTransformation = glm.scale(rotateZ, glm.vec3(scaleS, scaleS, scaleS))

    glUniformMatrix4fv(glGetUniformLocation(programMesh, "initialTransform"), 1, GL_FALSE,
                           glm.value_ptr(initialTransformation))

    print("initMeshStatic(): \n  ModelViewMesh: ", ModelViewMesh, "\n  ProjectionMesh: ", ProjectionMesh)

    # retrieve texture Sampler2D and init sampler with Texture Unit 0
    textureSampler = glGetUniformLocation(programMesh, "TextureSampler2D")
    glUniform1i(textureSampler, 0)

    glBindBuffer(GL_ARRAY_BUFFER, 0)


def displayMeshStatic():
    global programMesh
    global m_VAO

    global currentTime, lastTime, deltaTime

    global light_position
    global g_dir, g_quat
    global quatToMat

    global viewer_pos
    global g_ZoomX, g_ZoomY, g_Zoom
    global model_viewMesh
    global view_matrix
    global projection_matrix

    
    global ModelViewMesh
    global ProjectionMesh
    global LightPositionMesh

    glUseProgram(programMesh)
    glBindVertexArray(m_VAO)

    # Compute time difference between current and last frame
    lastTime = SDL_GetTicks() / 1000
    currentTime = SDL_GetTicks() / 1000
    deltaTime = 1. * (currentTime - lastTime)

    if wire:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # update light position
    for i in range(0, 3):
        light_position[i] = g_dir[i]

    # setup MV matrix including rotation from GUI
    quaternion = glm.quat(glm.vec3(g_quat[0], g_quat[1], g_quat[2]))
    quatToMat = glm.mat4_cast(quaternion)

    # generate new modelView matrix for each frame
    viewer_pos = glm.vec3(g_ZoomX, g_ZoomY, -g_Zoom)
    model_viewMesh = view_matrix * glm.translate(glm.mat4(1.), viewer_pos) * quatToMat

    glUniformMatrix4fv(ModelViewMesh, 1, GL_FALSE, glm.value_ptr(model_viewMesh))
    glUniformMatrix4fv(ProjectionMesh, 1, GL_FALSE, glm.value_ptr(projection_matrix))

    # pass the light position and direction
    glUniform4f(LightPositionMesh, light_position.x, light_position.y, light_position.z, light_position.w)

    # render()
    glDrawElements(GL_TRIANGLES, len(pMesh.faces) * 3, GL_UNSIGNED_INT, None)

    # For the next frame, the "last time" will be "now"
    lastTime = currentTime

    # glActiveTexture(GL_TEXTURE0)
    # glActiveTexture(GL_TEXTURE0)
     # glBindTexture(GL_TEXTURE_2D, textureSampler)

    glBindVertexArray(0)  


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

    print("\nYay! Initialized SDL successfully in basicCharacterApp!")
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
    window_title = 'basicCharacterApp'
    windowWidth = 1024
    windowHeight = 768
    gWindow = SDL_CreateWindow(window_title.encode(), SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,windowWidth, windowHeight, SDL_WINDOW_OPENGL )

    if gWindow is None:
        print("Window could not be created! SDL Error: ", SDL_GetError())
        raise RuntimeError('Failed to create SDL window')
        #exit(1)

    print("Yay! Created window successfully in basicCharacterApp!")
    gContext = SDL_GL_CreateContext(gWindow)
    print("Yay! Created OpenGL context successfully in basicCharacterApp!\n\n")
    
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



def displayGUI():
    global wire
    global color1
    global state
    global f

    global g_dir
    global g_ZoomX, g_ZoomY, g_Zoom
    global g_quat

    global direction
    global position
    global view_matrix

    # ImGui.new_frame()
    ImGui.set_next_window_size(200.0, 200.0)
    ImGui.set_next_window_position(10., 10.)
    ImGui.begin("Rendering Editor", True)

    # Creates a checkbox
    changed, checkbox = ImGui.checkbox("Wireframe", state)
    if checkbox is False:
        wire = False
        state = False
    if checkbox is True:
        wire = True
        state = True

    ImGui.separator()
    if ImGui.tree_node("LightDir"):
        changed, g_dir[0] = ImGui.slider_float("X", g_dir[0], -10., 10.)
        changed, g_dir[1] = ImGui.slider_float("Y", g_dir[1], -10., 10.)
        changed, g_dir[2] = ImGui.slider_float("Z", g_dir[2], -10., 10.)
        ImGui.tree_pop()

    ImGui.end()

    ImGui.begin("Scene Editor")
    ImGui.set_next_window_size(200., 200.)
    ImGui.set_next_window_position(220., 10.)

    if ImGui.tree_node("Viewer Position"):
        changed, g_ZoomX = ImGui.slider_float("Viewer X", g_ZoomX, -50., 100.)
        changed, g_ZoomY = ImGui.slider_float("Viewer Y", g_ZoomY, -150., 150.)
        changed, g_Zoom = ImGui.slider_float("Viewer Z", g_Zoom, -150., 1200.)
        ImGui.tree_pop()

    ImGui.separator()
    if ImGui.tree_node("Rotation"):
        changed, g_quat = ImGui.slider_float3("Rotate", *g_quat, 0., 2 * math.pi)
        ImGui.tree_pop()

    if ImGui.button("Reset View", 80, 20):
        g_ZoomX = 0.
        g_ZoomY = -50.
        g_Zoom = 300.

        g_quat = [0., 0., 0.]

        direction = glm.vec3(-1.3, -8.8, -30.)
        position = glm.vec3(-0.08, 5., -0.9) + direction * 0.2
        view_matrix = glm.lookAt(position, direction, glm.vec3(0., 2., 0.))

    ImGui.end()

def event_handler(event):
    global camx1, camx2
    global camy1, camy2
    global wire
    global g_ZoomX, g_ZoomY, g_Zoom
    global enable_move
    global horizontalAngle, verticalAngle
    global windowWidth, windowHeight
    global right, direction

    #if event.type == SDL_WINDOWEVENT:
       # if event.window.event:
     #       print('resize in progress')

    if event.type == SDL_MOUSEWHEEL:
        return True
    if event.type == SDL_TEXTINPUT:
        return True
    if event.type == SDL_KEYDOWN:
        if event.key.keysym.sym == SDLK_UP:
            camy1 = 1
            return True
        if event.key.keysym.sym == SDLK_DOWN:
            camy2 = 1
            return True
        if event.key.keysym.sym == SDLK_LEFT:
            camx1 = 1
            return True
        if event.key.keysym.sym == SDLK_RIGHT:
            camx2 = 1
            return True
        if event.key.keysym.sym == SDLK_w:
            if wire:
                wire = False
            else:
                wire = True
            return True
        if event.key.keysym.sym == SDLK_x:
            if event.key.keysym.mod & SDLK_CAPSLOCK:
                g_ZoomX -= 0.01
                if g_ZoomX < -50.:
                    g_ZoomX = -50.
            else:
                g_ZoomX += 0.01
                if g_ZoomX > 100.:
                    g_ZoomX = 100.
            return True
        if event.key.keysym.sym == SDLK_y:
            if event.key.keysym.mod & SDLK_CAPSLOCK:
                g_ZoomY -= 0.01
                if g_ZoomY < -150.:
                    g_ZoomY = -150.
            else:
                g_ZoomY += 0.01
                if g_ZoomY > 150.:
                    g_ZoomY = 150.
            return True
        if event.key.keysym.sym == SDLK_z:
            if event.key.keysym.mod & SDLK_CAPSLOCK:
                g_Zoom -= 0.01
                if g_Zoom < -150.:
                    g_Zoom = -150.
            else:
                g_Zoom += 0.01
                if g_Zoom > 150.:
                    g_Zoom = 150.
            return True
        if event.key.keysym.sym == SDLK_c:
            if enable_move:
                SDL_WarpMouseInWindow(gWindow, windowWidth // 2, windowHeight // 2)
                enable_move = 0
            else:
                enable_move = 1
            return True
        return True

    if event.type == SDL_KEYUP:
        if event.key.keysym.sym == SDLK_UP:
            camy1 = 0
            return True
        if event.key.keysym.sym == SDLK_DOWN:
            camy2 = 0
            return True
        if event.key.keysym.sym == SDLK_LEFT:
            camx1 = 0
            return True
        if event.key.keysym.sym == SDLK_RIGHT:
            camx2 = 0
            return True
        return True
    if event.type == SDL_MOUSEMOTION:
        if enable_move == 1:
            return True
        mouseX = event.motion.x
        mouseY = event.motion.y
        horizontalAngle += (windowWidth // 2 - mouseX) * 0.005
        verticalAngle += (windowHeight // 2 - mouseY) * 0.005
        right = glm.vec3(math.sin(horizontalAngle - 3.14 // 2.0), 0, math.cos(horizontalAngle - 3.14 // 2.0))
        direction = glm.vec3(math.cos(verticalAngle) * math.sin(horizontalAngle), math.sin(verticalAngle), math.cos(verticalAngle) * math.cos(horizontalAngle))

        return True
    return False

def camera_move():
    global enable_move
    global camx1, camx2, camy1, camy2, camz1, camz2
    global view_matrix
    global horizontalAngle
    global position
    global direction
    global gWindow
    global right

    if enable_move == 1:
        return

    right = glm.vec3(math.sin(horizontalAngle - 3.14 // 2.0), 0, math.cos(horizontalAngle - 3.14 // 2.0))
    if camx1:
        position -= right * 8.
    if camx2:
        position += right * 8.
    if camy1:
        position += direction * 8.
    if camy2:
        position -= direction * 8.
    if camz1:
        position = position + direction * 8.
    if camz2:
        position = position + direction * 8.
    view_matrix = glm.lookAt(position, direction + position, glm.cross(right, direction))
    SDL_WarpMouseInWindow(gWindow, windowWidth // 2, windowHeight // 2)


def main():
    """
    The main method that after calling init() it starts the main rendering loop.
    This loop re-draws a shader-based Cube, the ImGUI sample window in immediate mode and finally swaps the SDL2 double buffer windows
    """
    
    #run pyglm tests
    #GLMTests()
    
    global wireFrame
    global windowWidth
    global windowHeight
    global gWindow
    global gContext
    global bgColor
    global depthrenderbuffer
    global Screen_FBO
    global scene

    aflag = 0
    bflag = 0
    cvalue = None
    index = 0
    c = 0
    
    #scene = pyassimp.load(fileNameS, processing=pyassimp.postprocess.aiProcess_Triangulate)
    
    
    gWindow, gContext, gVersionLabel = init()
    
    if USE_MESH_STATIC:
        print('Initializing STATIC_MESH: ',fileNameS)
        initMeshStatic(fileNameS)
    #the model we load
    print("MODEL:" + fileNameS)
    print
    
    #write some statistics
    print("SCENE:")
    print("  meshes:" + str(len(scene.meshes)))
    print("  materials:" + str(len(scene.materials)))
    print("  textures:" + str(len(scene.textures)))
    print
   
    #  Enable depth test
    glEnable(GL_DEPTH_TEST)
    #  Accept fragment if it closer to the camera than the former one
    glDepthFunc(GL_LESS)
    #SDL_WarpMouseInWindow(gWindow, windowWidth // 2, windowHeight // 2)
    
    #ImGui.create_default_context(purpose=Purpose.SERVER_AUTH, cafile=None, capath=None, cadata=None)
    imguiContext = ImGui.create_context()
    
    if imguiContext is None:
        print("Window could not be created! ImGUI Error: ")
        exit(1)
    else:
        print("Yay! ImGUI context created successfully")
    renderer = SDL2Renderer(gWindow)
    
    event = SDL_Event()
    running = True
    # MAIN LOOP
    while running:
        while SDL_PollEvent(ctypes.byref(event)) != 0:
            event_handler(event)
            if event.type == SDL_KEYDOWN:
                if event.key.keysym.sym == SDLK_ESCAPE:
                    running = False
            if event.type == SDL_QUIT:
                running = False
            renderer.process_event(event)
        renderer.process_inputs()

         #ImGui.set_next_window_size(300.0, 150.0)
        # start new frame context
        ImGui.new_frame()
        
        camera_move()

        glViewport(0, 0, windowWidth, windowHeight)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(*bgColor)

        # bind our frame buffer to write
        # glBindRenderbuffer(GL_RENDERBUFFER, depthrenderbuffer)
        # glBindFramebuffer(GL_FRAMEBUFFER, Screen_FBO)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(*bgColor)
        
        if USE_MESH_STATIC:
            displayMeshStatic()
        
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
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
    pyassimp.release(scene)
    SDL_GL_DeleteContext(gContext)
    SDL_DestroyWindow(gWindow)
    SDL_Quit()
   


if __name__ == "__main__":
   main()





