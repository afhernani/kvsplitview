"""
Module archive.py
======================

This module contains the base class for all archive actions. Also
subclasses which implement some the base notifications functionality.

Classes:

* Copy: Action with predefined button set (['Ok', 'Cancel'])

* Move: Action with predefined button set (['Ok', 'Cancel'])

* Remove: Confirmation to Notification with predefined button set (['Yes', 'No'])

Copy class
==========

Move class
==========

Remove class
==========

"""
import os, sys
import shutil
from os.path import join
from functools import partial
from kivy import metrics, kivy_data_dir
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.properties import (ListProperty, StringProperty, NumericProperty,
    BoundedNumericProperty, BooleanProperty)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.uix.button import Button, Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.progressbar import ProgressBar
from kivy.logger import Logger
try:
    from .hbase import HBase
    from .file  import Folder
    from .notification import Notification, Message, Error, Confirmation
except:
    from file  import Folder
    from notification import Notification, Message, Error, Confirmation
    from hbase import HBase

__author__ = 'hernani'
__all__ = ('Copy', 'Move', 'Remove', 'Rename', 'Box')

class Archy(HBase):
    """Copy class. See module documentation for more information.
    """
    size_hint_x = NumericProperty(.9, allownone=True)
    size_hint_y = NumericProperty(.9, allownone=True)
    '''Default size properties for the popup
    '''
    title = StringProperty('Copy files ...')
    '''Default title for class
    '''
    path = StringProperty(u'/')
    '''Directory selcted
    '''
    BUTTON_SEARCH = 'Search'
    buttons = ListProperty([HBase.BUTTON_CANCEL, HBase.BUTTON_OK])
    '''Default button set for class
    '''
    files = ListProperty()
    '''This property represents the files on the popup.

    :attr:`files` is a :class:`~kivy.properties.ListProperty` and defaults to
    ''[]
    '''

    def __init__(self, **kwargs):
        self._pnl_files = None
        super(Archy, self).__init__(**kwargs)

    def _get_body(self):
        pnl = BoxLayout(orientation='vertical',padding=10, spacing=10 )
        self._pnl_files = BoxLayout(orientation='vertical', padding=10 ) #, size_hint_y=None)
        self.property('files').dispatch(self)
        scroll = ScrollView(size_hint_y=self.size_hint_y, height=300)
        scroll.add_widget(self._pnl_files)
        pnl.add_widget(scroll)
        #pnl.add_widget(self._pnl_files)
        self._pnl_path = BoxLayout(padding=10, spacing=10, size_hint_y=None, height=30)
        self.direction = TextInput(text=self.path, multiline=False, size_hint_y=None, height=30)
        self.bind(path=self.direction.setter('text'))
        # self.fbind(pnl, self.direction)
        self._pnl_path.add_widget(self.direction)
        self.btn_search = Button(text='...', size_hint_x=0.3, size_hint_y=None, height=30, on_release=self.search)
        # self.fbind(pnl, self.btn_search)
        self._pnl_path.add_widget(self.btn_search)
        pnl.add_widget(self._pnl_path)
        return pnl
    
    def on_files(self, instance, files):
        if self._pnl_files is None:
            return

        self._pnl_files.clear_widgets()
        if len(files) == 0:
            self._pnl_files.height = 0
            return
        self._pnl_files.size_hint_y=self.size_hint_y
        self._pnl_files.height = self._pnl_files.minimum_height
        for item in files:
            if isinstance(item, Box):
                name = os.path.basename(item.movie)
                image = os.path.basename(item.picture)
                label_v = Label(text=name, font_size=20, size_hint_y=None, height=30)
                # label_i = Label(text=image, font_size=20, size_hint_y=None, height=30)
                self._pnl_files.add_widget(label_v)
                # self._pnl_files.add_widget(label_i)
            else:
                name = os.path.basename(item)
                label = Label(text=name, font_size=20, size_hint_y=None, height=30)
                self._pnl_files.add_widget(label)

    def search(self, *args):
        Logger.warning(msg='procesando ...')
        Folder(on_dismiss=self.path_callback, path=self.path) # expanduser(u'~'))

    def path_callback(self, instance):
        Logger.warning(msg=instance.path)
        self.path = instance.path


class Copy(Archy):
    def _on_click(self, instance):
        """Pre-dismiss method.
        Gathers widget values. Checks the required fields.
        Ignores it all if the "Cancel" was pressed.
        """
        instance_id = instance.text
        if instance_id != self.BUTTON_CANCEL:
            Logger.warning(msg="write here for action copy files")
            if isinstance(self.files[0], Box):
                Logger.warning(msg="files with objets Box")
                path_image = os.path.join(self.path, "Thumbails")
                if not os.path.exists(path_image): os.makedirs(path_image)
                for item in self.files:
                    self.copy_box(item)
            else:
                for item in self.files:
                    self.copy_file(item)
        
        super(Copy, self)._on_click(instance)
    
    def copy_box(self, box, *args):
        video = os.path.basename(box.movie)
        new_video_path = os.path.join(self.path, video)
        caja = Box(movie=new_video_path)

        def copia(origen, destino, *args):
            try:
                shutil.copy(origen, destino)
            except IOError as e:
                Error(text='Don`t panic!. '+ str(e.args) + origen)
        
        try:
            Clock.schedule_once(partial(copia, box.movie, caja.movie), -1)
            Clock.schedule_once(partial(copia, box.picture, caja.picture), -1)
        except Exception as e:
            Error(text='Don`t panic!. '+ str(e.args))

    def copy_file(self, archivo, *args):

        origen = os.path.abspath(archivo)
        filename = os.path.basename(origen) #origen.split('\\')[-1]
        
        def copia(origen, destino, *args):
            try:
                shutil.copy(origen, destino)
            except IOError as e:
                Error(text='Don`t panic!. '+ str(e.args) + origen)
        
        if self.path:
            try:
                Clock.schedule_once(partial(copia, origen, join(self.path, filename)), -1)
            except Exception as e:
                Error(text='Don`t panic!. '+ str(e.args))
                # XMessage(text=str(e.args), title='Message Exception')


class Move(Archy):
    def _on_click(self, instance):
        """Pre-dismiss method.
        Gathers widget values. Checks the required fields.
        Ignores it all if the "Cancel" was pressed.
        """
        instance_id = instance.text
        if instance_id != self.BUTTON_CANCEL:
            Logger.warning(msg="write here for action copy files")
            if isinstance(self.files[0], Box):
                Logger.warning(msg="files with objets Box")
                path_image = os.path.join(self.path, "Thumbails")
                if not os.path.exists(path_image): os.makedirs(path_image)
                for item in self.files:
                    self.move_box(item)
            else:
                for item in self.files:
                    self.move_file(item)
        
        super(Move, self)._on_click(instance)
    
    def move_box(self, box, *args):
        video = os.path.basename(box.movie)
        new_video_path = os.path.join(self.path, video)
        caja = Box(movie=new_video_path)

        def mueve(origen, destino, *args):
            try:
                shutil.move(origen, destino)
            except IOError as e:
                Error(text='Don`t panic!. '+ str(e.args) + origen)

        try:
            Clock.schedule_once(partial(mueve, box.movie, caja.movie), -1)
            Clock.schedule_once(partial(mueve, box.picture, caja.picture), -1)
        except Exception as e:
            Error(text='Don`t panic!. '+ str(e.args))

    def move_file(self, archivo, *args):

        origen = os.path.abspath(archivo)
        filename = os.path.basename(origen)

        def mueve(origen, destino, *args):
            try:
                shutil.move(origen, destino)
            except IOError as e:
                Error(text='Don`t panic!. '+ str(e.args) + origen)
        
        if self.path:
            try:
                Clock.schedule_once(partial(mueve, origen, join(self.path, filename)), -1)
            except Exception as e:
                Error(text='Don`t panic!. '+ str(e.args))


class Remove(Archy):
    def _get_body(self):
        pnl = super(Remove, self)._get_body()
        self.btn_search.disabled = True
        self.direction.disabled = True
        return pnl

    def _on_click(self, instance):
        """Pre-dismiss method.
        Gathers widget values. Checks the required fields.
        Ignores it all if the "Cancel" was pressed.
        """
        instance_id = instance.text
        if instance_id != self.BUTTON_CANCEL:
            Logger.warning(msg="write here for action copy files")
            if isinstance(self.files[0], Box):
                Logger.warning(msg="files with objets Box")
                for item in self.files:
                    self.remove_file(item.movie)
                    self.remove_file(item.picture)
            else:
                for item in self.files:
                    self.remove_file(item)
        super(Remove, self)._on_click(instance)

    def remove_file(self, archivo, *args):
        
        origen = os.path.abspath(archivo)
               
        def remove(origen, *args):
            try:
                os.remove(origen)
            except IOError as e:
                Error(text='Don`t panic!. '+ str(e.args) + origen, title='Message Exception')

        if self.path:
            try:
                Clock.schedule_once(partial(remove, origen, ), -1)
            except Exception as e:
                Error(text='Don`t panic! '+ str(e.args), title='Message Exception')
        else:
            Error(text='Do not exist directory. '+ str(self.path), title='Message Exception')


class Rename(Archy):
    name = StringProperty('')
    def _get_body(self):
        pnl = super(Rename, self)._get_body()
        self.unbind(path=self.direction.setter('text'))
        self.bind(name=self.direction.setter('text'))
        self.btn_search.disabled = True
        if isinstance(self.files[0], Box):
            self.name = os.path.basename(self.files[0].movie)
        else:
            self.name = os.path.basename(self.files[0])
        # self.direction.text = self.files[0]
        #self.direction.disabled = True
        return pnl

    def _on_click(self, instance):
        """Pre-dismiss method.
        Gathers widget values. Checks the required fields.
        Ignores it all if the "Cancel" was pressed.
        """
        instance_id = instance.text
        if instance_id != self.BUTTON_CANCEL:
            Logger.warning(msg="write here for action copy files")
            self.name = self.direction.text
            if isinstance(self.files[0], Box):
                self.rename_file(self.files[0].movie)
                self.name = self.name + '_thumbs_0000.gif'
                self.rename_file(self.files[0].picture)
            else:
                self.rename_file(self.files[0])
        super(Rename, self)._on_click(instance)

    def rename_file(self, archivo, *args):

        origen = os.path.abspath(archivo)
        self.path = os.path.dirname(origen)
        # filename = os.path.basename(origen)
        new_file_name = self.name

        def mueve(origen, destino, *args):
            try:
                shutil.move(origen, destino)
            except IOError as e:
                Error(text='Don`t panic!. '+ str(e.args) + origen)
        
        if self.path:
            try:
                Clock.schedule_once(partial(mueve, origen, join(self.path, new_file_name)), -1)
            except Exception as e:
                Error(text='Don`t panic!. '+ str(e.args))


class Box(object):

    def __init__(self, movie=None, picture=None, **kvargs):
        self.seted = False
        self.movie = movie
        self.picture = picture
        if self.movie is None and self.picture is not None:
            self.setmovie()
        elif self.movie is not None and self.picture is None:
            self.setpicture()
        else:
            self.seted = True
        super(Box, self).__init__()
    
    def setmovie(self):
        
        filenameimage = os.path.basename(self.picture)
        pathfileimage = os.path.dirname(self.picture)
        ops = pathfileimage.split(os.sep)
        ops2 = ops[:len(ops)-1]
        pathfilevideo = os.sep.join(ops2)
        filenamevideo = filenameimage.split('_thumbs_')[0]
        self.movie = os.path.join(pathfilevideo, filenamevideo)
        self.seted = True

    def setpicture(self):
        
        filenamevideo = os.path.basename(self.movie)
        pathfilevideo = os.path.dirname(self.movie)
        pathfileimage = os.path.join(pathfilevideo, 'Thumbails')
        filenameimage = filenamevideo + '_thumbs_0000.gif'
        self.picture = os.path.join(pathfileimage, filenameimage)
        self.seted = True

    def __str__(self, *args):
        return "{ \"video\":" + f" {self.movie}, " + "\"picture\":"+ f" {self.picture}"+" }"

    def __repr__(self, *args):
        return self.__str__()

# comprobaciones.

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from os.path import expanduser
class TestApp(App):
    def build(self):
        label = BoxLayout()
        label.add_widget(Button(text='copy', on_release=self.btncopy))
        label.add_widget(Button(text='move', on_release=self.btnmove))
        label.add_widget(Button(text='remove', on_release=self.btnremove))
        label.add_widget(Button(text='rename', on_release=self.btnrename))
        label.add_widget(Button(text='Box', on_release=self.boxes))
        return label

    def btncopy(self, *args):
        files = ['perro.png']
        # files.extend(dir(App))
        Copy(files=files, on_dismiss=self.my_callback, path=os.getcwd())
    
    def btnmove(self, *args):
        files = ['perro.png']
        # files.extend(dir(App))
        Move(title='Move files to...',files=files, 
                on_dismiss=self.my_callback, path=os.getcwd())

    def btnremove(self, *args):
        files = ['perro.png', 'ccccccc.mp4', 
                    'ttttttt-oooo.mp3', 'sosa.txt', 'yeshua.sue', 
                    'tortola.tor', 'mi_paso.xo', 'otro_mas']
        # files.extend(dir(App))
        Remove(title='Remove files ...', files=files, path=os.getcwd() ) #, on_dismiss=self.my_callback)

    def btnrename(self, *args):
        files = ['perro.png']
        Rename(title="Rename file", files=files, path=os.getcwd())

    def my_callback(self, instance):
        if instance.is_canceled():
            return
        s_message = 'Pressed button: %s\n\n' % instance.button_pressed

        Logger.info(msg=s_message)
        
    def boxes(self, *args):
        video = '/media/hernani/WDatos/tmp/_Asian_baby/7eddd05f7c77ace2e996c99a8740f6c0.mp4'
        picture = '/media/hernani/WDatos/tmp/_Asian_baby/Thumbails/26d59945395e045e8ea79a0969d71140.mp4_thumbs_0000.gif'
        box = Box(movie=video)
        box1 = Box(picture=picture)
        print(box)
        print(box1)
        boxlist = [box, box1]
        print(boxlist)


if __name__ == '__main__':
    TestApp().run()