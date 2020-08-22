"""
ffpeglib package.
Usefull extensions of the ffmpeg class

Package Structure
=================

Modules:

* __init__.py: API imports


"""

__author__ = 'hernani'
__email__ = 'afhernani@gmail.com'
__apply__ = 'library kvcomic'
__version__ = '0.3'

try:
    from .moviebox import Boxd, MovieBox
    from .videostream import VideoStream
except:
    from moviebox import Boxd, MovieBox
    from videostream import VideoStream

