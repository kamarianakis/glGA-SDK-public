# **glGA SDK**

## *version 2020.1*

## a **g**eometry and a**l**gebra SDK for computer **G**raphics **A**lgorithms and applications with emphasis on virtual character animation, rendering, deformation

---

### *Copyright 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, all Rights Reserved*

### *Prof. George Papagiannakis, papagian@csd.uoc.gr*

### *University of Crete & Foundation for Research & Technology - Hellas (FORTH)*

---

> **New decade, new languages, new tools**:
> cross platform compilation (cmake), cross platform/programming language development with (VSCode) employing Python, C++ and C# for a computer graphics (CG) full-stack deployment ( GPU to CPU character rendering and animation) to realise cross-operating system, cross-game engine, cross-algebra CG character algorithm development. This a `Rosetta stone` approach based on *literate programming*, i.e. writing documentation that contains the same code in different systems: e.g. a jupyter notebook showing basic GPU shader-based programming in Python, C++ and C#.

### **A. glGA SDK Requirements**

**A scientific development/experimentation/visualization and algorithmic design/teaching computation platform** from *CPU to GPU CG and XR* and from *euclidean, quaternion algebra to geometric algebra GA* and *deep learning (DL) for computer graphics (CG)*:

- shader based OpenGL4.4 complete pipeline support: vertex, fragment, geometry, compute, tessellation shaders
- Geometric algebra as an all-in-one framework unifying linear algebra, complex numbers, Quat, Dquat algebras
- Window toolkits across multiple operating systems
- 2D GUIs easy to setup and parameterize
- Common 3D file formats such as .dae and .fbx
- GLSL style mathematics library for shader-based math
- Python2GPU avenues
  - Convert Python to C++ or Cuda
  - Embed the python interpreter in C++
- Vulkan support for low level GPU
- GPGPU programming support for:
  - OpenCL
  - CUDA
  - AMD ROCm
- OpenVR access to steamVR library for basic VR cross VR-HMD support
- Jupyter notebooks for literate programming, CG algorithmic exploration and teaching
  1. CG Character Rendering
     1. Path tracing (*Shirley's "Ray tracing in a Weekend" and SmallPT*)
     2. Phong Lighting and Shading with point lights
     3. Camera and Object linear transformations
     4. Image Based Lighting
     5. SH area lights with rotation
     6. Precomputed Radiance Transfer
  2. CG Character animation
     1. keyframe animation & blending
     2. Linear blend skinning
     3. Dual quaternion skinning
  3. Geometric Algebra (GA) for Computer Graphics (CG)
      1. GA motors (EGA, CGA and rotation, translation, dilation)
      2. GA quaternion blending
      3. GA skinning
      4. GA PRT
      5. GA Cutting
      6. GA Tearing
      7. GA drilling

### **B. glGA SDK main features**

1. `Full-stack CG development`: same code-base across languages and platforms: from python to C++ and from C# and Unity to C++ and Unreal with same basic CG examples from CPU rendering to GPU shader languages.
2. `Basic glGA examples for introductory CG` programming in:
   1. C++, OpenGL in glGA 5.0
   2. Python, OpenGL in glGA SDK 2020
   3. C#, OpenGL/Dx in Unity
   4. C++, OpenGL in Unreal
3. `Path tracing` with smallPT/ray tracing in a weekend
   1. C++ smallPT
   2. Python smallPT
   3. C# smallPT
   4. python RayTracing from P. Shirley
4. `Support for source control & elegant code` documentation
   1. Github flow
   2. Github submodules
   3. Python intro to scientific computing
   4. Readthedocs Sphinx project
5. `Support shader-based CG examples` in glGA
   1. BasicWindow
   2. BasicCubeGUI
   3. BasicPhong
   4. OpenGL Orange book GLSL chapters
   5. glGACharacterApp
       - Vertex specification
       - Mesh loading
       - Texturing
       - Character Animation
       - Skinning
       - GA interpolation, animation, skinning
       - VR simulation
       - All OpengL GPU shader pipeline:
         - Vertex
         - Fragment
         - Geometry
         - Compute
         - Tesselation
           - <https://stackoverflow.com/questions/24083656/tessellation-shader-opengl>
6. `Support geometric algebra for CG character simulation` in glGA
    - Gaigen GA on shaders
    - glGAMesh
    - glGAMath
7. `Support shader-based Unity CG examples`
    - Same glGA basic shader examples in C# and Cg (similar to glGA but for Unity)
    - Monte Carlo Path Tracing using compute shaders in Unity (BSc thesis)
8. Support for `python 2 GPU` pathways
   1. Python2cpp via pybind (module) - and then via C# wrapper to Unity -
   2. Embed the python interpreter
      1. <https://pybind11.readthedocs.io/en/stable/advanced/embedding.html>
      2. <https://docs.python.org/3.5/extending/embedding.html#pure-embedding>
      3. Python->Cmake embedded python in Cpp->wrapper C# for Unity!
   3. Use pybind11 C++ API to call python
      1. <https://pybind11.readthedocs.io/en/stable/advanced/pycpp/object.htmlUse>
   4. Cpp2python
      1. pybind11 to call C++ from python (e.g. glGAMath, glGAMesh classes)
         - Insight: Python is great for pedagogical experimentation.
         - However, once the algorithm is identified, C++ has to be employed, as it is far more efficient and GPU/VR friendly
         - <https://stackoverflow.com/questions/45054860/extending-c-to-python-using-pybind11>
         - <https://stackoverflow.com/questions/11866288/importing-a-pyd-created-with-swig-in-python-2-7-3-on-mac>
   5. Python2cuda via numba (module)
      - <https://developer.nvidia.com/auth0/callback?destination=how-to-cuda-python&code=jYyBdhhHrr43MYUQ&state=login>
      - <http://numba.pydata.org/numba-doc/latest/user/5minguide.html>
      - <https://github.com/ContinuumIO/gtc2020-numba>
   6. Use Cython to create a C dynamic libray that contains the python modules
      - <http://docs.cython.org/en/latest/src/tutorial/external.html>
      - Python2compute shader via gaigen (module)
   7. Using the unity/unreal python embedded console (2.7) (jupyter instructions)
   8. Using Unity’s ML agents external communicator module  (jupyter instructions)
   9. Rebuild unreal engine with Python 3.7 support (instead of 2.7)
9. `Third party lib support python for data science, CG, GPU and GA` development:
   1. Jupyter (anaconda, visual studio code)
   2. numba (conda)
   3. Clifford (conda)
   4. galgebra (pip)
   5. Numpy (conda)
   6. Matplotlib (conda)
   7. Scipy (conda)
   8. Scikit-learn (conda)
   9. Tensorflow (conda)
   10. Keras (conda)
   11. Pybind11 (github)
   12. Cython (pip)
   13. Scientific-python-lectures (submodule, github)
   14. Python CG libraries:
       1. pyOpenGL/pyOpenGL-accelerate (pip)
           1. <http://pyopengl.sourceforge.net/context/tutorials/shader_1.html>
           2. <https://github.com/rougier/python-opengl>
           3. <http://morpheo.inrialpes.fr/~franco/3dgraphics/practical1.html>
       2. pySDL2 (pip)
       3. pyImGUI (pip)
       4. pyGLM (pip)
       5. pyAssimp (pip) (first assimp via macports)
       6. Libigl (conda)
       7. Pyigl (pip)
       8. vulkan (pip)
       9. Pyopencl (github)
          1. Example in Lecture_6b_hpc from python scientific computing notebook
       10. pyopenvr (github and pip)
           1. Has been updated to latest steamvr 1.11.11
       11. Imageio (conda)
       12. Pybullet(pip)
       13. Tqdm progress bar (pip)
   15. Third party C++/CUDA physics libraries:
       1. PositionBAsedDyanmics
           1. <https://github.com/InteractiveComputerGraphics/PositionBasedDynamics.git>
           2. <https://github.com/Scrawk/Position-Based-Dynamics.git>
       2. VIPER
          1. <https://github.com/vcg-uvic/viper.git>
       3. SphereTree
          1. <https://github.com/mlund/spheretree.git>
       4. Bullet (pybullet) conda
   16. Third party open source CG frameworks for multiOS support
       1. Magnum (magnum.graphics)
           1. <https://doc.magnum.graphics/magnum/getting-started.html>

> ### Notes
>
>- To get pyassimp to work:
>   - Install first latest assimp via macports: sudo port install assimp (version 5.0)
>   - Add opt/local/lib on helper.py (where the assimp library is)
>     - assimp/port/PyAssimp/pyassimp/structs.py
>       - Line 1088 in 0adc032
>         - ("mPrivate", c_char_p),
>         - Deleting that line resolves the error.
>     - Previous glGA cpp framework 5.0 is a submodule
>       - It can be build as cpp inside visual studio code: <https://medium.com/audelabs/> c-development-using-visual-studio-code-cmake-and-lldb-d0f13d38c563>
>- Readthedocs project:
> - <https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html>
>- Python/Cpp/C# development:
>   - visual studio code with python, cpp, c#, cmake, gitlens, github plugins
>   - Kite and kite copilot for python docs and intellisense (www.kite.com)

### **C. References**

1. Papaefthymiou M. et al. (2017) Gamified AR/VR Character Rendering and Animation Enabling Technologies. In: Ioannides M., Magnenat-Thalmann N., Papagiannakis G. (eds) Mixed Reality and Gamification for Cultural Heritage. Springer, Cham.
2. Papaefthymiou, M., Hildenbrand, D., & Papagiannakis, G. (2016). An inclusive Conformal Geometric Algebra GPU animation interpolation and deformation algorithm. Visual Computer, 32(6-8), 1–9. <http://doi.org/10.1007/s00371-016-1270-8>
3. Papaefthymiou, M., Feng, A., Shapiro, A., Papagiannakis, G., “A fast and robust pipeline for populating mobile AR scenes with gamified virtual characters”. ACM SIGGRAPH-ASIA 2015, Symposium On Mobile Graphics and Interactive Applications, Kobe, ACM Press, November 2015
4. Papagiannakis, G., Papanikolaou, P., Greassidou, E., & Trahanias, P. E. (2014). glGA: an OpenGL Geometric Application Framework for a Modern, Shader-based Computer Graphics Curriculum. (pp. 9–16), Eurographics 2014, <http://doi.org/10.2312/eged.20141026>
5. Papagiannakis, G. (2013). Geometric algebra rotors for skinned character animation blending. Technical Brief, ACM SIGGRAPH ASIA 2013, Hong Kong, November 2013, 1–6.

### **D. Contributors**

- Prof. George Papagiannakis
- Papanikolaou Petros
- Greassidou Elisavet
- Georgiou Stylianos
- Kateros Stavros
- Zikas Pavlos
- Lydatakis Nikolaos
- Papaefthymiou Margarita
- Kanakis Marios
- Bachlitzanakis Vasileios
- Geronikolakis Stratos
- Evangellou Yannis
- Kartsonaki Ioanna

---

## **APPENDICES**

## A. Why now in Python

Our objective in this SDK is two-fold:

- a) we want to teach, learn and expriment with key CG and underlying algebraic concepts as efficiently as possible, more than achieving absolute highest framerates. C/C++ are powerful but cluttered, error-prone low-level languages, that get in the way of this learning efficiency.
- b) we want to provide rapid prototyping, algorithmic understanding, experimentation and code equivalence between Python, C++ and C# across CPU and GPU frameworks and the two most prevailing, modern game engines (Unity and Unreal).
- c) we want to emphasize on *"literate programming"* and Python-Jupyter notebooks are the best current vehicle for that IMHO: "In literate programming the emphasis is reversed. Instead of writing code containing documentation, the literate programmer writes documentation containing code. No longer does the English commentary injected into a program have to be hidden in comment delimiters at the top of the file, or under procedure headings, or at the end of lines. Instead, it is wrenched into the daylight and made the main focus. The "program" then becomes primarily a document directed at humans, with the code being herded between "code delimiters" from where it can be extracted and shuffled out sideways to the language system by literate programming tools." <http://www.literateprogramming.com/index.html>

e.g. OpenGL is primarily a C API which for most CG applications today is actually used with C++ (or C#) in the industry. There are many good reasons for that: often the goal is to have the fastest possible code on the CPU side, since rendering for real-time visualization means that a *frame needs to be produced onscreen every 10, 16 or 33 milliseconds (for 100Hz, 60Hz, 30Hz refresh rates) and no time can be wasted*.

- Python code is more straightforward, easier to read, write, and debug
- It is less verbose (typically by a factor of 5-10 on the code size), and benefits from an extensive and intuitive set of built-ins (tuples, lists, dictionaries, arrays…)
- In particular Python constructs, like generators, list and dictionary comprehensions are a great way to reduce simple object construction loops to one readable line of code, or create iterators that unclutter the code. Keep those in mind when you write your application.
- Well written Python code can be quite fast already, and most inner loop tasks of interest to these practicals happen on the GPU anyway, once properly initialized.
- What’s more, Python has excellent wrappers to OpenGL and window libraries whose interface closely match their C counterpart. Which means anything you learn about writing code in Python directly maps to the C APIs.
- Python is already the programming language of choice for deep learning algortihms and data science in general, with numerous libraries and frameworks.
- Python is already being adopted by latest versions of 3D game engines, such as Unity and Unreal.

---

## B. glGA Folder Structure Outline

- glGA-SDK:
  - Readme
  - License
  - .gitignore
  - vscode/
    - #*contains vsCode workspace, macPorts list of third party libraries and python virtual environment list of conda and pip packages and modules*
  - doc/
    - #*contains literate programming notebooks with documentation that include code in a Rosetta Stone approach where possible*
    - CG/
      - RealtimeRendering/
      - RealtimeAnimation/
      - RealtimeDeformation/
      - CGnotes
    - GI/
      - rayTracing
      - smallPT
    - Computing/
      - jupyterJunonotebooks
    - GA/
      - GATE/
    - py2GPU/
      - Py2cpp/
      - Py2numba/
      - Py2csharp/
    - DLGA/
      - deepLearning
        - jupyterDLnotebook
      - embodiedAI
    - Physics/
  - SDK/
    - python/
      - glGA/
        - Helper
        - Mesh
        - RigMesh
        - Math
        - KDTree
        - PRT
      - dlGA/
        - #*deep learning for graphics algorithms and applications*
      - Apps/
        - BasicExamples/
        - AdvancedExamples/
        - AssignmentExamples/
        - OrangeBookExamples/
    - cpp/
      - lib/
      - bin/
      - thirdPartyLibs
    - frameworks
      - cpp/
        - Submodule: glGA/
        - Submodule: GAE/
      - python/
        - Submodule: MR-GRAIL/
      - unity/
        - Submodule: UnityXR-edu/
      - unreal/
        - Submodule: Unreal basic shader projects (TBD in future)
  - extern/
    - python/
      - computing
        - Submodule: pybind11
        - Submodule: scientific-python-lectures
        - Submodule: numerical computing with python
        - Submodule: pyopencl
      - GA
        - Submodule: clifford
        - Submodule: galgebra
      - CG
        - Submodule: pyopengl
        - Submodule: pyimgui
        - Submodule: pysdl2
        - Submodule: tqdm
        - Submodule: pyGLM
      - deepLearning
        - Submodule: glassner deep learning1
        - Submodule: glassner deep learning2
      - GI
        - Submodule:numpy-smallpt
        - Submodule:raytracing-in-one-weekend-python
    - Cpp/
      - computing
        - Submodule:modern-cpp-features
        - Submodule:learning-cMake
        - Submodule:GLM
      - GI
        - Submodule:rayTracing
        - Submodule:cpp-smallpt
        - Submodule:spherical-harmonics
      - physics
        - Submodule:Spheretree
        - Submodule:Pbd
        - Submodule:Bullet3
    - cSharp/
      - GI
        - Submodule:cs-smallpt
        - Submodule:cs-raytracing

## *C. Release notes*

- **17/05/20** initial github repository: <https://github.com/papagiannakis/glGA-SDK.git>
- **05/06/20** version 0.1 with all submodules setup
- **24/07/20** updated submodules
