"""
Module notifybase.py
======================

This module contains the base class for all notifications. Also
subclasses which implement some the base notifications functionality.

Classes:

* XNotifyBase: Base class for all notifications.


XNotifyBase class
=================

Subclass of :class:`hpopup.HBase`.
The base class for all notifications. Also you can use this class to create
your own notifications::

    NotifyBase(title='You have a new message!', text='What can i do for you?',
                buttons=['Open it', 'Mark as read', 'Remind me later'])

Or that way::

    class MyNotification(NotifyBase):
        buttons = ListProperty(['Open it', 'Mark as read', 'Remind me later'])
        title = StringProperty('You have a new message!')
        text = StringProperty('What can i do for you?')
    popup = MyNotification()

.. note:: :class:`Message` and :class:`Error` classes were created in a
    similar manner. Actually, it is just a subclasses with predefined default
    values.

Similarly for the :class:`Confirmation` class. The difference - it has
:meth:`Confirmation.is_confirmed` which checks which button has been
pressed::

    def my_callback(instance):
        if instance.is_confirmed():
            print('You are agree')
        else:
            print('You are disagree')
    popup = Confirmation(text='Do you agree?', on_dismiss=my_callback)


"""

from os.path import join
from kivy import metrics, kivy_data_dir
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.properties import (ListProperty, StringProperty, NumericProperty,
    BoundedNumericProperty, BooleanProperty)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.uix.progressbar import ProgressBar
from kivy.uix.label import Label
from kivy.logger import Logger
try:
    from .hbase import HBase
except:
    from hbase import HBase

__author__ = 'Hernani'

__all__ = ('NotifyBase')

class NotifyBase(HBase):
    """NotifyBase class. See module documentation for more information.
    """

    text = StringProperty('')
    '''This property represents text on the popup.

    :attr:`text` is a :class:`~kivy.properties.StringProperty` and defaults to
    ''.
    '''

    dont_show_text = StringProperty('Do not show this message again')
    '''Use this property if you want to use custom text instead of
    'Do not show this message'.

    :attr:`text` is a :class:`~kivy.properties.StringProperty`.
    '''

    dont_show_value = BooleanProperty(None, allownone=True)
    '''This property represents a state of checkbox 'Do not show this message'.
    To enable checkbox, set this property to True or False.

    .. versionadded:: 0.2.1

    :attr:`dont_show_value` is a :class:`~kivy.properties.BooleanProperty` and
    defaults to None.
    '''

    def __init__(self, **kwargs):
        self._message = Label(text=self.text)
        self.bind(text=self._message.setter('text'))
        super(NotifyBase, self).__init__(**kwargs)

    def _get_body(self):
        if self.dont_show_value is None:
            return self._message
        else:
            pnl = BoxLayout(orientation='vertical')
            pnl.add_widget(self._message)

            pnl_cbx = BoxLayout(
                size_hint_y=None, height=metrics.dp(35), spacing=5)
            cbx = CheckBox(
                active=self.dont_show_value, size_hint_x=None,
                width=metrics.dp(50))
            cbx.bind(active=self.setter('dont_show_value'))
            pnl_cbx.add_widget(cbx)
            pnl_cbx.add_widget(
                Label(text=self.dont_show_text, halign='left'))

            pnl.add_widget(pnl_cbx)
            return pnl


# comprobaciones.

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from os.path import expanduser
class TestApp(App):
    def build(self):
        label = BoxLayout()
        label.add_widget(Button(text='open', on_release=self.btnopen))
        return label

    def btnopen(self, *args):
        NotifyBase(title='You have a new message!', text='What can i do for you?',
                buttons=['Open it', 'Mark as read', 'Remind me later'], on_dismiss=self.my_callback)
        
    def my_callback(self, instance):
        if instance.is_canceled():
            return
        s_message = 'Pressed button: %s\n\n' % instance.button_pressed
        try:
            values = instance.values
            for kw in values:
                s_message += ('<' + kw + '> : ' + str(values[kw]) + '\n')
        except AttributeError:
            pass

        Logger.info(msg=s_message)
        
        
if __name__ == '__main__':
    TestApp().run()