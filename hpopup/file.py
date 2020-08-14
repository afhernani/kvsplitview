"""
Module file.py
==============

.. versionadded:: 0.1

This module contains the class which represents
:class:`~kivy.uix.filechooser.FileChooser` in the popup and some templates
for this class.

Classes:

* Folder: :class:`FilePopup` template for folder selection.

* FileOpen: :class:`FilePopup` template for files selection.

* FileSave: :class:`FilePopup` template for save file.


Folder class
=============

Subclass of :class:`hpopup.FilePopup`.
This class is a template with predefined property values for selecting
the folders. He also checks the validity of the selected values. In this case,
selection is allowed only folders.

By default the folder selection is disabled. It means that the folder cannot be
selected because it will be opened by one click on it. In this case the
selected folder is equal to the current path.

By the way, the folder selection is automatically enabled when you set
:attr:`FilePopup.multiselect` to True. But in this case the root folder
cannot be selected.


FileOpen class
===============

Subclass of :class:`hpopup.FilePopup`.
This class is a template with predefined property values for selecting
the files. He also checks the validity of the selected values. In this case,
selection is allowed only files.


FileSave class
===============

Subclass of :class:`popup.FilePopup`.
This class is a template with predefined property values for entering name of
file which will be saved.
It contains the :class:`~kivy.uix.textinput.TextInput` widget for input
filename.

To set a default value in the TextInput widget, use :attr:`FileSave.filename`.
Also this property can be used to get the file name entered.

To get full filename (including path), use :meth:`FileSave.get_full_name`.

Following example shows how to use properties::

    def my_callback(instance):
        print(u'Path: ' + instance.path)
        print(u'Filename: ' + instance.filename)
        print(u'Full name: ' + instance.get_full_name())

    popup = FileSave(filename='file_to_save.txt', on_dismiss=my_callback)

"""


from kivy import metrics
from kivy.factory import Factory
from kivy.properties import StringProperty, NumericProperty, ListProperty,\
    OptionProperty, BooleanProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.logger import Logger
from os import path, makedirs
try:
    from .filepopup import FilePopup
except:
    from filepopup import FilePopup

__author__ = 'ophermit, hernani'

__all__ = ('FileSave', 'FileOpen', 'Folder')

class FileSave(FilePopup):
    """FileSave class. See module documentation for more information.
    """

    BUTTON_SAVE = 'Save'
    TXT_ERROR_FILENAME = 'Maybe you should enter a filename?'

    filename = StringProperty(u'')
    '''Represents entered file name. Can be used for setting default value.
    '''

    title = StringProperty('Save file')
    '''Default title for the popup
    '''

    buttons = ListProperty([BUTTON_SAVE, FilePopup.BUTTON_CANCEL])
    '''Default button set for the popup
    '''

    def _get_body(self):
        txt = TextInput(text=self.filename, multiline=False,
                        size_hint_y=None, height=metrics.dp(30))
        txt.bind(text=self.setter('filename'))
        self.bind(filename=txt.setter('text'))

        layout = super(FileSave, self)._get_body()
        layout.add_widget(txt)
        return layout

    def on_selection(self, *largs):
        if len(self.selection) == 0:
            return

        if not self.browser.file_system.is_dir(self.selection[0]):
            self.filename = self.selection[0].split(path.sep)[-1]

    def dismiss(self, *largs, **kwargs):
        """Pre-validation before closing.
        """
        if self.button_pressed == self.BUTTON_SAVE:
            if self.filename == '':
                # must be entered filename
                Logger.exception(msg=self.TXT_ERROR_FILENAME)
                # XError(text=self.TXT_ERROR_FILENAME)
                return self

        return super(FileSave, self).dismiss(*largs, **kwargs)

    def get_full_name(self):
        """Returns full filename (including path)
        """
        return self.path + path.sep + self.filename


class FileOpen(FilePopup):
    """FileOpen class. See module documentation for more information.
    """

    BUTTON_OPEN = 'Open'
    TXT_ERROR_SELECTION = 'Maybe you should select a file?'

    title = StringProperty('Open file')
    '''Default title for the popup
    '''

    buttons = ListProperty([BUTTON_OPEN, FilePopup.BUTTON_CANCEL])
    '''Default button set for the popup
    '''

    def dismiss(self, *largs, **kwargs):
        """Pre-validation before closing.
        """
        if self.button_pressed == self.BUTTON_OPEN:
            self._filter_selection(folders=False)
            if len(self.selection) == 0:
                # files must be selected
                Logger.exception(msg=self.TXT_ERROR_SELECTION)
                # XError(text=self.TXT_ERROR_SELECTION)
                return self
        return super(FileOpen, self).dismiss(*largs, **kwargs)


class Folder(FilePopup):
    """Folder class. See module documentation for more information.
    """

    BUTTON_SELECT = 'Select'
    TXT_ERROR_SELECTION = 'Maybe you should select a folders?'

    title = StringProperty('Choose folder')
    '''Default title for the popup
    '''

    buttons = ListProperty([BUTTON_SELECT, FilePopup.BUTTON_CANCEL])
    '''Default button set for the popup
    '''

    def __init__(self, **kwargs):
        super(Folder, self).__init__(**kwargs)
        # enabling the folder selection if multiselect is allowed
        self.filters.append(self._is_dir)
        if self.multiselect:
            self.dirselect = True

    def _is_dir(self, directory, filename):
        return self.browser.file_system.is_dir(path.join(directory, filename))

    def dismiss(self, *largs, **kwargs):
        """Pre-validation before closing.
        """
        if self.button_pressed == self.BUTTON_SELECT:
            if not self.multiselect:
                # setting current path as a selection
                self.selection = [self.path]

            self._filter_selection(files=False)
            if len(self.selection) == 0:
                # folders must be selected
                Logger.exception(msg=self.TXT_ERROR_SELECTION)
                # XError(text=self.TXT_ERROR_SELECTION)
                return self
        return super(Folder, self).dismiss(*largs, **kwargs)



#### comprobaciones.

from kivy.app import App
from os.path import expanduser
class TestApp(App):
    def build(self):
        label = BoxLayout()
        label.add_widget(Button(text='Folder', on_release=self.btnfolder))
        label.add_widget(Button(text='Fileopen', on_release=self.btnfileopen))
        label.add_widget(Button(text='Filesave', on_release=self.btnfilesave))
        return label

    def btnfolder(self, *args):
        popup = Folder(on_dismiss=self.my_callback, path=expanduser(u'~'))

    def btnfileopen(self, *args):
        FileOpen(on_dismiss=self.my_callback, path=expanduser(u'~'),
                  multiselect=True)

    def btnfilesave(self, *args):
        popup = FileSave(filename='file_to_save.txt', 
                        path=expanduser(u'~'), 
                        on_dismiss=self.my_callback)

        
    def my_callback(self, instance):
        try:
            print(u'Path: ' + instance.path)
            print(u'Selection: ' + str(instance.selection))

            print(u'Path: ' + instance.path)
            print(u'Filename: ' + instance.filename)
            print(u'Full name: ' + instance.get_full_name())
        except Exception as e:
            Logger.warning(msg=str(e.args))


if __name__ == '__main__':
    TestApp().run()
