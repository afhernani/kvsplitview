#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
import os, sys
import threading
import kivy
kivy.require('1.9.0')
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from hoverable import HoverBehavior
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.clock import Clock, mainthread
from kivy.core.window import Window
from kivy.config import ConfigParser, Config
from kivy.graphics import Line
import configparser
from kivy.properties import StringProperty
from hpopup import Copy, Move, Remove, Rename, Box

__author__='hernani'
__email__ = 'afhernani@gmail.com'
__apply__ = 'kvcomic app for gif about viedo in carpet'
__version__ = 0.1

class Splitfloat(HoverBehavior, Image):
    def __init__(self, **kwargs):
        self.selected = None
        super(Splitfloat, self).__init__(**kwargs)
        # self.source = '629_1000.jpg'

    def on_press(self):
        # self.source = 'atlas://data/images/defaulttheme/checkbox_on'
        pass

    def on_release(self):
        # self.source = 'atlas://data/images/defaulttheme/checkbox_off'
        pass

    def on_touch_down(self, touch):
        # (x, y)=self.to_widget(touch.x, touch.y)
        ''' if self.collide_point(x, y):
            if touch.is_double_tap:
                print('double touch', 'action here', self.source)
                return True '''
        if self.collide_point(touch.x, touch.y):
            if not self.selected:
                self.select()
            else:
                self.unselect()
            self.touched = True
            if touch.is_double_tap:
                print('double:', self.source)
                from utility import lunch_video_default
                lunch_video_default(self.source)
            return True
        return super(Splitfloat, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        # x, y = touch.x, touch.y
        # (x, y)=self.parent.to_parent(touch.x, touch.y)  
        (x, y)=self.to_widget(touch.x, touch.y)
        # print(x, y)
        if self.collide_point(x, y):
            print('true')
            return True
        return super(Splitfloat, self).on_touch_move(touch)

    def on_enter(self, *args):
        print("You are in, though this point", self.border_point, self.source)
        self.anim_delay= 1

    def on_leave(self, *args):
        print("You left through this point", self.border_point, self.source)
        self.anim_delay= -1

    def select(self):
        print('select()', self.top)
        if not self.selected:
            self.ix = self.center_x
            self.iy = self.center_y
            with self.canvas.before:
                # self.Color(rgb=(1,0,0))
                self.selected = Line(rectangle=
                    (self.x, self.y, self.width, self.height), dash_offset=2, color=(1,0,0), width=10)

    def unselect(self):
        print('unselect()')
        if self.selected:
            self.canvas.before.remove(self.selected)
            self.selected = None


Builder.load_string('''
<ContentSplits>:
    orientation:'vertical'
    ScrollView:
        BoxLayout:
            id:box
            orientation:'horizontal'
            height: self.minimum_height
            size_hint_x:None
            width: self.minimum_width
            padding: '20dp', '20dp'
            spacing: '20dp'
    BoxLayout:
        height:'30sp'
        size_hint_y:None
        Button:
            text:'Open'
            size_hint_x:None
            width: '60sp'
            on_release:app.get_running_app().show_load()
        Button:
            text:'Move'
            size_hint_x:None
            width:'60sp'
            on_release:app.get_running_app().move_selected()
        Button:
            text:'Copy'
            size_hint_x:None
            width:'60sp'
            on_release:app.get_running_app().copy_selected()
        Label:
            id:lbnota
            text:'...'
            size_hint_x:None
            width: '60sp'
<Splitfloat>:
    anim_delay: 1 if self.hovered else -1
    allow_stretch: True
    # pos: 200,200
    # size_hint: None, None
    size: '300sp', '200sp'
    size_hint_x: None
    # height: '300dp'
    # with: '300dp'
    font_size: '20dp'
    # canvas.before:
    #    Color:
    #        rgb: 1,1,1
    #    Rectangle:
    #        size: self.size
    #        pos: self.pos
    # Image:
    #    pos: root.pos
    #    size: root.size
    #    source: 'bbw.gif'
<LoadDialog>:
    BoxLayout:
        size: root.size
        pos: root.pos
        orientation:'vertical'
        FileChooserListView:
            id: filechooser
            multiselect: True
            path:'.'
        BoxLayout:
            size_hint_y: None
            height:sp(30)
            Button:
                text:'Cancel'
                on_release:root.cancel()
            Button:
                text:'Load'
                on_release: root.load(filechooser.path, filechooser.selection)
    
    ''')

class ContentSplits(BoxLayout):
    files=[]
    def __init__(self, files=[], **kwargs):
        super(ContentSplits, self).__init__(**kwargs)
        self.files = files
        for file in self.files:
            # img = Image(source=file, anim_delay=1)
            self.ids.box.add_widget(Splitfloat(source=file, anim_delay=1))
    
    def addfile(self):
        print('addfile:', self.files)
        box = BoxLayout(orientation='vertical',padding=10,spacing=10)
        botones = BoxLayout(padding=10,spacing=10, size_hint_y=None, height=30)
        
        self.filechooser = FileChooserListView()
        # self.filechooser.height = 400 # this is a bit ugly...
        self.filechooser.path='.'

        box.add_widget(self.filechooser)
        
        pop = Popup(title='Select Directory',content=box,size_hint=(None,None),
                    size=(400,600))

        si = Button(text='Si',on_release=self.on_load, height='30dp', width='20dp')
        no = Button(text='No',on_release=pop.dismiss, height='30dp', width='20dp')
        botones.add_widget(si)
        botones.add_widget(no)
        box.add_widget(botones)

        pop.open()
        # print('select', self.filechooser.selection)
        
    

from kivy.properties import ObjectProperty

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    
class SampleApp(App):
    # stop = threading.Event()
    setingfile = 'seting.ini'
    title ='Splitfloat'
    path_job = StringProperty(None)
    
    def build(self):
        self.files=[]
        self.box = ContentSplits(files=self.files)
        # box.ids.box.add_widget(Splitfloat(source='mica.gif',anim_delay= 1))
        self.get_init_status()
        return self.box

    def selected_splitfloat(self, *args):
        '''busca los splitfloats selecioado y devuelve una lista con los objetos'''
        boxes = self.box.ids.box
        childrens= boxes.children[:]
        selected =[]
        for child in childrens:
            if child.selected:
                selected.append(child)
                child.unselect()
        return selected

    def copy_selected(self, *args):
        '''copy splitfloat to ... '''
        selected = self.selected_splitfloat()
        all_archives = self._createlistselected(selected=selected)
        if self.path_job is None:
            self.path_job =os.path.dirname(all_archives[0].movie)
        for item in all_archives:
            print('selected ->>', item)
        Copy(files=all_archives, on_dismiss=self.my_callback, path=self.path_job)

    def move_selected(self, *args):
        '''move splitfloats to ...'''
        selected = self.selected_splitfloat()
        all_archives = self._createlistselected(selected=selected)
        if self.path_job is None:
            self.path_job =os.path.dirname(all_archives[0].movie)
        for item in all_archives:
            print('selected ->>', item)
        Move(files=all_archives, on_dismiss=self.my_callback, path=self.path_job)
        for child in selected: self.box.ids.box.remove_widget(child)

    def my_callback(self, instance):
        self.path_job = instance.path

    def _createlistselected(self, selected=[])->[]:
        todos_los_archivos =  []
        for item in selected:
            box = Box(picture=item.source)
            todos_los_archivos.append(box)
        return todos_los_archivos

    def dismiss_popup(self, *args):
        self.popup.dismiss()
    
    def show_load(self):
        contenido=LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self.popup= Popup(title='Selct Directory', content=contenido, size_hint=(.9,.9))
        self.popup.open()

    def load(self, path, filenames):
        self.popup.dismiss()
        self.dirpathmovies = path
        # for filename in filenames:
        #    with open(os.path.join(path, filename)) as cadena:
        #        self.files.append(filename)
        # print('files:', self.files)
        print('path:', path, 'filenames:', filenames)
        self.files=[]
        threading.Thread(target=self.load_thread, daemon=True).start()
        # pasando con argumentos, .
        # threading.Thread(target=self.load_thread, args=(argumeto,), daemon=True).start()

    def load_thread(self, *args):
        from functools import partial
        self.total = 0
        dirpathmovies = self.dirpathmovies
        self.title = 'Splitfloat :: ' + dirpathmovies
        print('dirpathmovies:', dirpathmovies)
        exten = ('.gif', '.GIF')
        dirthumbs = os.path.join(dirpathmovies, 'Thumbails')
        print('dirthumbs:', dirthumbs)
        self.box.ids.box.clear_widgets()
        if os.path.exists(dirthumbs):
            for fe in os.listdir(dirthumbs):
                if fe.endswith(exten):
                    fex = os.path.abspath(os.path.join(dirthumbs, fe))
                    print(fex)
                    self.files.append(fex)
                    # Clock.schedule_once(partial(self.update_box_imagen, str(fex)), 0.5)
                    # self.box.ids.box.add_widget(Splitfloat(source=fex, anim_delay= 1))
        self.title += r' :: ' + str(len(self.files))
        threading.Thread(target=self.start_load_thread, args=(self.files,), daemon=True).start()

    def start_load_thread(self, files=[]):
        from time import sleep
        try:
            for file in files:
                self.update_box_imagen(file)
                sleep(0.5)
        except:
            print('exception in start load thread from app')
    
    total = 0
    
    @mainthread
    def update_box_imagen(self, file, *largs):
        self.box.ids.box.add_widget(Splitfloat(source=file, anim_delay= -1))
        # title = 'Splitfloat :: ' + self.dirpathmovies + ' :: ' + str(len(self.files))
        # print('>> long: ', title)
        self.total += 1
        self.box.ids.lbnota.text = str(self.total)

    def get_init_status(self):
        '''
        extract init status of app
        Return:
        '''
        if not os.path.exists(self.setingfile):
            return
        config = configparser.RawConfigParser()
        config.read(self.setingfile)
        self.dirpathmovies = config.get('Setings', 'dirpathmovies')
        if os.path.exists(self.dirpathmovies):
            # inicializa la lista con directorio duardao
            # threading.Thread(target=self.load_thread, daemon=True).start()
            self.load_thread()

    def on_stop(self):
        '''
        write init status of app
        Return:
        '''
        config = configparser.RawConfigParser()
        config.add_section('Setings')
        config.set('Setings', 'dirpathmovies', self.dirpathmovies)
        config.set('Setings', 'sizewindow', self.sizewindow)
        with open(self.setingfile, 'w') as configfile:
            config.write(configfile)
        print('Write config file')
    
    sizewindow =''
    
    def on_resize(self, instancie, width, height):
        '''Event called when the window is resized'''
        print(f'window.size {str(width)}, {str(height)}')
        print(f'instancie: {instancie.top}, {instancie.left}')
        self.sizewindow = str(width)+'x'+ str(height) + 'x' + str(instancie.top) + 'x' + str(instancie.left)
        print('variable: '+ self.sizewindow)
        
    def get_sizewindow(self, cadena):
        '''descomponer la cadena de dimensiones de la ventana'''
        return cadena.split('x')

    from kivy.core.window import Window

    def on_start(self, **kvargs):
        ''' lunch after build and start window '''
        Window.bind(on_resize=self.on_resize)
        # Window.bind(on_motion=self.on_motion_thumbapp)
        # Window.bind(on_draw=self.on_draw_thumbapp)
        Window.bind(on_request_close=self.on_request_close)
        # self._keyboard = Window.request_keyboard(self._keyboard_closed, self, 'text')
        Window.bind(on_keyboard=self.on_keyboard)
        # print('on_start')
        if not os.path.exists(self.setingfile):
            return
        config = configparser.RawConfigParser()
        config.read(self.setingfile)
        try:
            self.sizewindow = config.get('Setings', 'sizewindow')
            w, h, t, l = self.get_sizewindow(self.sizewindow)
            # print(w, h, t, l)
            Window.size = (int(w), int(h))
            Window.Top = int(t)
            Window.left = int(l)
        except Exception:
            print('exception load sizewindow')

    def on_request_close(self, *args):
        self.textpopup(title='Exit', text='Are you sure?')
        return True

    def textpopup(self, title='', text=''):
        """Open the pop-up with the name.
 
        :param title: title of the pop-up to open
        :type title: str
        :param text: main text of the pop-up to open
        :type text: str
        :rtype: None
        """
        box = BoxLayout(orientation='vertical')
        box.add_widget(Label(text=text))
        mybutton = Button(text='OK', size_hint=(1, 0.25))
        box.add_widget(mybutton)
        popup = Popup(title=title, content=box, size_hint=(None, None), size=(300, 200))
        mybutton.bind(on_release=self.stop) # manda detener la aplicación
        popup.open()

    def on_keyboard(self, keyboard, key, text, modifiers, *args):
        print(f'{keyboard}, {key}, {text}, {modifiers}, {args}')
        return True


if __name__ == '__main__':
    SampleApp().run()


"""
Image(
source= 'image.gif', 
anim_delay= 0,
mipmap= True,
allow_stretch= True)

I believe this may help you, I had a series of png files that I wanted to animate into an 
explosion, and this was a game where the explosions were constant. Initially, every time 
the animation took place, the game stalled and stuttered horribly. This is what I did to get 
my game to run smoothly. I zipped the png files, and used the following code to preload them, 
which I placed in the __init__ method of the Screen widget that the images appeared on.

load_zipped_png_files = Image(
    source = 'explosion.zip', 
    anim_delay = 0,
    allow_stretch = True, 
    keep_ratio = False,
    keep_data = True)

I believe the keep_data option allows for the preloading of the 
images( into a cache I imagine ), which saves the program from having to reload 
them every time they are used.

Now it could be that I am mistaken about the role keep_data is playing here 
( and if someone reading this knows better, please do correct me ), but zipping 
the files and using them in this way definitely made the animations acceptably smooth. 
You could test it with and without keep_data = True and figure it out yourself.

"""
