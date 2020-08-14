"""
ffpeglib package.
Usefull extensions of the ffmpeg class

Package Structure
=================

Modules:

* __init__.py: API imports

"""
try:
    from .moviebox import Boxd, MovieBox
except:
    from moviebox import Boxd, MovieBox

__author__ = 'hernani'
__version__ = '0.0.1'
