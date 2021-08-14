# glGA SDK
## version 2021.0.5

a geometry and algebra SDK for computer Graphics Algorithms and applications with emphasis on virtual character animation, rendering, deformation

### Copyright 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, all Rights Reserved

Prof. George Papagiannakis, papagian@csd.uoc.gr
University of Crete & Foundation for Research & Technology - Hellas (FORTH)

This is the `pyglGA` package.
In order to locally install it via pip, please go one folder up and exsecute:
`python -m pip install -e .`

## Platform Specific Notes

### MacOS Big Sur

For OpenGL support on Big Sur, please follow the following steps:
- pip install PyOpenGL and PyOpenGL-accelerate
- follow the fix described here: https://github.com/simnibs/simnibs/issues/47 

To get pyassimp to work:
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
> 