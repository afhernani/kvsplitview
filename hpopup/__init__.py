"""
hPopup package.
Usefull extensions of the Popup class

Package Structure
=================

Modules:

* __init__.py: API imports

"""
try:
    from .hpopup import HPopup
    from .hbase import HBase
    from .filepopup import FilePopup
    from .file  import FileSave, FileOpen, Folder
    from .notifybase import NotifyBase
    from .notification import Notification, Message, Error, Confirmation
    from .progress import Progress, Loading
    from .form import HSlider, HTextInput, Notes, Authorization
    from .archive import Copy, Move, Remove, Rename, Box
except:
    from hpopup import HPopup
    from hbase import HBase
    from filepopup import FilePopup
    from file  import FileSave, FileOpen, Folder
    from notifybase import NotifyBase
    from notification import Notification, Message, Error, Confirmation
    from progress import Progress, Loading
    from form import HSlider, HTextInput, Notes, Authorization
    from archive import Copy, Move, Remove, Rename, Box

__author__ = 'hernani'
__version__ = '0.0.1'
