"""
Module filepopup.py
==============

.. versionadded:: 0.3

This module contains the class which represents
:class:`~kivy.uix.filechooser.FileChooser` in the popup and some templates
for this class.

Classes:

* FilePopup: represents :class:`~kivy.uix.filechooser.FileChooser` in the
  popup.


FilePopup class
================

Subclass of :class:`hpopup.HBase`.
This class represents :class:`~kivy.uix.filechooser.FileChooser` in the
popup with following features:

* label which shows current path

* buttons which allows you to select view mode (icon/list)

* button `New folder`

Usage example::

    popup = FilePopup(title='FilePopup demo', buttons=['Select', 'Close'])

To set path on the filesystem that this controller should refer to, you can
use :attr:`FilePopup.path`. The same property you should use to get the
selected path in your callback.

By default it possible to select only one file. If you need to select multiple
files, set :attr:`FilePopup.multiselect` to True.

By default it possible to select files only. If you need to select the
files and folders, set :attr:`FilePopup.dirselect` to True.

To obtain selected files and/or folders you need just use
:attr:`FilePopup.selection`.

You can add custom preview filters via :attr:`FilePopup.filters`

Following example shows how to use properties::

    def my_callback(instance):
        print(u'Path: ' + instance.path)
        print(u'Selection: ' + str(instance.selection))

    from os.path import expanduser
    popup = FilePopup(title='FilePopup demo', buttons=['Select', 'Close'],
                       path=expanduser(u'~'), on_dismiss=my_callback,
                       multiselect=True, dirselect=True)

"""

from kivy import metrics
from kivy.factory import Factory
from kivy.properties import (StringProperty, NumericProperty, ListProperty,
    OptionProperty, BooleanProperty, ObjectProperty )
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from os import path, makedirs
try:
    from .hbase import HBase
except:
    from hbase import HBase

__author__ = 'Hernani'

__all__ = ('FilePopup')


class FilePopup(HBase):
    """FilePopup class. See module documentation for more information.
    """

    size_hint_x = NumericProperty(1., allownone=True)
    size_hint_y = NumericProperty(1., allownone=True)
    '''Default size properties for the popup
    '''

    browser = ObjectProperty(None)
    '''This property represents the FileChooser object. The property contains
    an object after creation :class:`xpopup.FilePopup` object.
    '''

    path = StringProperty(u'/')
    '''Initial path for the browser.

    Binded to :attr:`~kivy.uix.filechooser.FileChooser.path`
    '''

    selection = ListProperty()
    '''Contains the selection in the browser.

    Binded to :attr:`~kivy.uix.filechooser.FileChooser.selection`
    '''

    multiselect = BooleanProperty(False)
    '''Binded to :attr:`~kivy.uix.filechooser.FileChooser.multiselect`
    '''

    dirselect = BooleanProperty(False)
    '''Binded to :attr:`~kivy.uix.filechooser.FileChooser.dirselect`
    '''

    filters = ListProperty()
    '''Binded to :attr:`~kivy.uix.filechooser.FileChooser.filters`
    '''

    CTRL_VIEW_ICON = 'icon'
    CTRL_VIEW_LIST = 'list'
    CTRL_NEW_FOLDER = 'new_folder'

    control_views = {'Icons': CTRL_VIEW_ICON, 'List': CTRL_VIEW_LIST, 'New folder': CTRL_NEW_FOLDER}

    view_mode = OptionProperty(
        CTRL_VIEW_ICON, options=(CTRL_VIEW_ICON, CTRL_VIEW_LIST))
    '''Binded to :attr:`~kivy.uix.filechooser.FileChooser.view_mode`
    '''

    def _get_body(self):
        from kivy.lang import Builder
        import textwrap
        self.browser = Builder.load_string(textwrap.dedent('''\
        FileChooser:
            FileChooserIconLayout
            FileChooserListLayout
        '''))

        self.browser.path = self.path
        self.browser.multiselect = self.multiselect
        self.browser.dirselect = self.dirselect
        self.browser.filters = self.filters
        self.browser.bind(path=self.setter('path'),
                          selection=self.setter('selection'))
        self.bind(view_mode=self.browser.setter('view_mode'),
                  multiselect=self.browser.setter('multiselect'),
                  dirselect=self.browser.setter('dirselect'),
                  filters=self.browser.setter('filters'))

        lbl_path = Label(
            text=self.browser.path, valign='top', halign='left',
            size_hint_y=None, height=metrics.dp(25))
        self.browser.bind(path=lbl_path.setter('text'))

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self._ctrls_init())
        layout.add_widget(lbl_path)
        layout.add_widget(self.browser)
        return layout

    def _ctrls_init(self):
        pnl_controls = BoxLayout(size_hint_y=None, height=metrics.dp(25))
        pnl_controls.add_widget(Button(
            text='Icons',
            on_release=self._ctrls_click))
        pnl_controls.add_widget(Button(
            text='List',
            on_release=self._ctrls_click))
        pnl_controls.add_widget(Button(
            text='New folder',
            on_release=self._ctrls_click))
        return pnl_controls

    def _ctrls_click(self, instance):
        instance_id = self.control_views.get(instance.text, None)
        if instance_id in self.property('view_mode').options:
            self.view_mode = instance_id
        elif instance_id == self.CTRL_NEW_FOLDER:
            TextInput(title='Input folder name',
                       text='New folder',
                       on_dismiss=self._create_dir)

    def _create_dir(self, instance):
        """Callback for create a new folder.
        """
        if instance.is_canceled():
            return
        new_folder = self.path + path.sep + instance.get_value()
        if path.exists(new_folder):
            text='Folder "%s" is already exist. Maybe you should enter another name?' % instance.get_value()
            print(text)
            return True
        makedirs(new_folder)
        self.browser.property('path').dispatch(self.browser)

    def _filter_selection(self, folders=True, files=True):
        """Filter the list of selected objects

        :param folders: if True - folders will be included in selection
        :param files: if True - files will be included in selection
        """
        if folders and files:
            return

        t = []
        for entry in self.selection:
            if entry == '..' + path.sep:
                pass
            elif folders and self.browser.file_system.is_dir(entry):
                t.append(entry)
            elif files and not self.browser.file_system.is_dir(entry):
                t.append(entry)
        self.selection = t



# comprobaciones.

from kivy.app import App
from os.path import expanduser
class TestApp(App):
    def build(self):
        label = BoxLayout()
        label.add_widget(Button(text='open', on_release=self.btnopen))
        return label

    def btnopen(self, *args):
        popup = FilePopup(title='FilePopup demo', buttons=['Select', 'Close'],
                       path=expanduser(u'~'), on_dismiss=self.my_callback,
                       multiselect=True, dirselect=True)
        #popup.bind(on_dismiss=self.my_callback)
        popup.open()
        
    def my_callback(self, instance):
        print(u'Path: ' + instance.path)
        print(u'Selection: ' + str(instance.selection))
        
if __name__ == '__main__':
    TestApp().run()
