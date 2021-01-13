"""
Utilities helper functions, components, part of the glGA SDK ECS
    
glGA SDK v2020.1 ECS (Entity Component System)
@Coopyright 2020 George Papagiannakis
    
The Compoment class is the dedicated to a specific type of data container in the glGA ECS.

The following is example restructured text doc example
:param file_loc: The file location of the spreadsheet
:type file_loc: str
:returns: a list of strings representing the header columns
:rtype: list

"""

# Python built-in modules
import math
from numbers import Number

# Python external modules
import numpy as np

# vector, points related functions -----------------------------------------------
def vec(*iterable):
    """
    return a numpy vector out of any iterable (list, tuple...) as column-major ('F')
    """
    return np.asarray(iterable if len(iterable) > 1 else iterable[0],dtype=np.float, order='F')

def normalise(vector):
    """standard vector normalization over any numpy array

    :param vector: iterable vector to normalise
    :type vector: numpy array
    """
    #norm = math.sqrt(vector*vector)
    if isinstance(vector, np.ndarray)==False:
        vector = vec(vector)
    norm = np.linalg.norm(vector,2) #equivalent to norm = np.sqrt(np.sum(vector**2))
    return vector / norm if norm >0. else vector

def lerp(point_a, point_b, fraction):
    """standard linear interpolation between two vectors and a fraction value

    :param point_a: first point
    :type point_a: numpy array
    :param point_b: second point
    :type point_b: numpy array
    :param fraction: value t
    :type fraction: float from 0.0 to 1.0
    :return: linearly interpolated value
    :rtype: numpy array
    """
    
    if isinstance(point_a, np.ndarray)==False:
        point_a = vec(point_a)
    if isinstance(point_b, np.ndarray)==False:
        point_b = vec(point_b)
    try:
        fraction = float(fraction)
    except ValueError:
        print (f'HEY! {fraction} is not a float!')
    
    return point_a + fraction * (point_b - point_a)

# ------------ convenience CG functions for vector, matrix and camera transformations --------------

def identity(rank=4):
    """generate a numpy identity matrix

    :param rank: [description], defaults to 4 for 4x4 matrix, otherwise 3 for 3x3 or 2 for 2x2
    :type rank: int, optional
    """
    if(rank == 4):
        return np.identity(4)
    elif (rank == 3):
        return np.identity(3)
    elif (rank == 2):
        return np.identity(2)
    elif (rank < 2 and rank > 4):
        return np.identity(4)
    
def ortho(left, right, bottom, top, near, far):
    """ Orthographic projection matrix creation function, where 
    the viewing volume is a rectangular parallelepiped, or more informally, a box. 
    Original projection matrices defined in http://www.glprogramming.com/red/appendixf.html
    and in http://www.glprogramming.com/red/chapter03.html. Tested also again glm similar 
    functions.
    
    :param left: [coordinates of projection unit cube]
    :type left: [float]
    :param right: [coordinates of projection unit cube]
    :type right: [float]
    :param bottom: [coordinates of projection unit cube]
    :type bottom: [float]
    :param top: [coordinates of projection unit cube]
    :type top: [float]
    :param near: [coordinates of near clipping plane]
    :type near: [float]
    :param far: [coordinates of far clipping plane]
    :type far: [float]
    """
    dx, dy, dz = right - left, top - bottom, far - near
    rx, ry, rz = -(right+left) / dx, -(top+bottom) / dy, -(far+near) / dz
    return np.array([
                    [2/dx, 0,    0,     rx],
                     [0,    2/dy, 0,     ry],
                     [0,    0,    -2/dz, rz],
                     [0,    0,    0,     1]
                     ], dtype=np.float,order='F')
    
def perspective(fovy, aspect, near, far):
    """Perspective projection matrix creation function, where 
    the viewing volume is a truncated pyramid. 
    Original projection matrices defined in http://www.glprogramming.com/red/appendixf.html
    and in http://www.glprogramming.com/red/chapter03.html and 
    https://www.khronos.org/registry/OpenGL-Refpages/gl2.1/xhtml/gluPerspective.xml 
    Tested also again glm similar functions.

    :param fovy: [description]
    :type fovy: [type]
    :param aspect: [description]
    :type aspect: [type]
    :param near: [description]
    :type near: [type]
    :param far: [description]
    :type far: [type]
    """
    #_scale = 1.0/math.tan(math.radians(fovy)/2.0)
    _scale = 1.0/math.tan(math.radians(fovy/2.0))
    sx, sy = _scale / aspect, _scale
    zz = (far + near) / (near - far)
    zw = 2 * far * near/(near - far)
    return np.array([[sx, 0,  0,  0],
                     [0,  sy, 0,  0],
                     [0,  0, zz, zw],
                     [0,  0, -1,  0]], dtype=np.float,order='F')
    
def frustum(xmin, xmax, ymin, ymax, zmin, zmax):
    """Alternative Perspective projection matrix creation function, where 
    the viewing volume is a truncated pyramid. 
    Original projection matrices defined in http://www.glprogramming.com/red/appendixf.html
    and in http://www.glprogramming.com/red/chapter03.html and 
    https://www.khronos.org/registry/OpenGL-Refpages/gl2.1/xhtml/gluPerspective.xml 
    Tested also again glm similar functions.

    :param xmin: [description]
    :type xmin: [type]
    :param xmax: [description]
    :type xmax: [type]
    :param ymin: [description]
    :type ymin: [type]
    :param ymax: [description]
    :type ymax: [type]
    :param zmin: [description]
    :type zmin: [type]
    :param zmax: [description]
    :type zmax: [type]
    """
    a = (xmax+xmin) / (xmax-xmin)
    b = (ymax+ymin) / (ymax-ymin)
    c = -(zmax+zmin) / (zmax-zmin)
    d = -2*zmax*zmin / (zmax-zmin)
    sx = 2*zmin / (xmax-xmin)
    sy = 2*zmin / (ymax-ymin)
    return np.array([[sx, 0,  a, 0],
                     [0, sy,  b, 0],
                     [0,  0,  c, d],
                     [0,  0, -1, 0]], dtype=np.float,order='F')
    

def translate(x=0.0, y=0.0, z=0.0):
    """ Convert a euclidean translation vector in homogeneous coordinates to a 
    standard 4x4 Translation Transformation matrix based on the original OpenGL formulas defined in:
    http://www.glprogramming.com/red/appendixf.html and OpenGL 1.0 specification. 
    The matrix will be created either from 3 euclidean coordinates or a vector x: vec(x)

    :param x: [description], defaults to 0.0
    :type x: float, optional or vec
    :param y: [description], defaults to 0.0
    :type y: float, optional
    :param z: [description], defaults to 0.0
    :type z: float, optional
    """
    Tmat = np.identity(4, np.float32)
    #Tmat[0,3] = x
    #Tmat[1,3] = y
    #Tmat[2,3] = z
    if isinstance(x, Number):
        Tmat[:3,3] = vec(x,y,z)  
    else:
         Tmat[:3,3] = vec(x)
    
    return Tmat


def scale(x, y=None, z=None):
    """Convert a euclidean scaling vector in homogeneous coordinates to a 
    standard 4x4 Scaling Transformation matrix based on the original OpenGL formulas defined in:
    http://www.glprogramming.com/red/appendixf.html and OpenGL 1.0 specification. 
    The matrix will be created either from 3 euclidean coordinates for scaling in 3 dimensions 
    or a vector x: vec(x) for uniform scaling across x,y,z dimensions

    :param x: [description], defaults to 1.0
    :type x: float, optional
    :param y: [description], defaults to None
    :type y: [type], optional
    :param z: [description], defaults to None
    :type z: [type], optional
    """
    x, y, z = (x, y, z)  if isinstance(x, Number) else (x[0], x[1], x[2])
    y, z = (x, x) if y is None or z is None else (y, z) # case of uniform scaling if y, z are None
    return np.diag((x, y, z, 1))


def sincos(degrees=0.0, radians=None):
    """Utility function to calculate with one call sine and cosine of an angle in radians or degrees
    If there is one argument, then assumes that single input is in degrees, 
    otherwise ignores first value and takes second for radians (needs two in that case)
    It returns the value in radians, first sin then cos
    
    :param degrees: [description], defaults to 0.0
    :type degrees: float, optional
    :param radians: [description], defaults to None
    :type radians: [type], optional
    """
    radians = radians if radians else math.radians(degrees)
    return math.sin(radians), math.cos(radians) 

def rotate(axis=(1.0,0.0,0.0), angle=0.0, radians=None):
    """From a euclidean axis vector and a rotation angle, generate a 
    standard 4x4 Rotation Transformation matrix based on the original OpenGL formulas defined in:
    http://www.glprogramming.com/red/appendixf.html and axis-angle theoretical matrix specification:
    https://en.wikipedia.org/wiki/Rotation_matrix  

    :param axis: [description], defaults to (1.0,0.0,0.0)
    :type axis: tuple, optional
    :param angle: [description], defaults to 0.0
    :type angle: float, optional
    :param radians: [description], defaults to None
    :type radians: [type], optional
    """
    x, y, z = normalise(vec(axis))
    s, c = sincos(angle, radians)
    nc = 1 - c
    return np.array([[x*x*nc + c,   x*y*nc - z*s, x*z*nc + y*s, 0],
                     [y*x*nc + z*s, y*y*nc + c,   y*z*nc - x*s, 0],
                     [x*z*nc - y*s, y*z*nc + x*s, z*z*nc + c,   0],
                     [0,            0,            0,            1]], dtype=np.float,order='F')