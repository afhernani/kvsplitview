"""
Module notification.py
======================

This module contains the base class for all notifications. Also
subclasses which implement some the base notifications functionality.

Classes:

* Message: Notification with predefined button set (['Ok'])

* Error: Message with predefined title

* Confirmation: Notification with predefined button set (['Yes', 'No'])

* Notification: Notification without buttons. Can autoclose after few
  seconds.

* Progress: Notification with ProgressBar

Notification class
===================

Subclass of :class:`popup.NotifyBase`.
This is an extension of :class:`NotifBase`. It has no buttons and can
be closed automatically::

    Notification(text='This popup will disappear after 3 seconds',
                  show_time=3)

If you don't want that, you can ommit :attr:`Notification.show_time` and
use :meth:`Notification.dismiss`::

    popup = Notification(text='To close it, use the Force, Luke!')
    def close_popup():
        popup.dismiss()

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
from kivy.logger import Logger
try:
    from .notifybase import NotifyBase
except:
    from notifybase import NotifyBase

__author__ = 'ophermit, Hernai'
__all__ = ('Notification', 'Message', 'Error', 'Confirmation')

class Notification(NotifyBase):
    """Notification class. See module documentation for more information.
    """

    show_time = BoundedNumericProperty(0, min=0, max=100, errorvalue=0)
    '''This property determines if the pop-up is automatically closed
    after `show_time` seconds. Otherwise use :meth:`Notification.dismiss`

    :attr:`show_time` is a :class:`~kivy.properties.NumericProperty` and
    defaults to 0.
    '''

    def open(self, *largs):
        super(Notification, self).open(*largs)
        if self.show_time > 0:
            Clock.schedule_once(self.dismiss, self.show_time)


class Message(NotifyBase):
    """MessageBox class. See module documentation for more information.
    """

    buttons = ListProperty([NotifyBase.BUTTON_OK])
    '''Default button set for class
    '''


class Error(Message):
    """ErrorBox class. See module documentation for more information.
    """

    title = StringProperty('Something went wrong...')
    '''Default title for class
    '''


class Confirmation(NotifyBase):
    """Confirmation class. See module documentation for more information.
    """

    buttons = ListProperty([NotifyBase.BUTTON_YES, NotifyBase.BUTTON_NO])
    '''Default button set for class
    '''

    title = StringProperty('Confirmation')
    '''Default title for class
    '''

    def is_confirmed(self):
        """Check the `Yes` event

        :return: True, if the button 'Yes' has been pressed
        """
        return self.button_pressed == self.BUTTON_YES


#### comprobaciones. #######################

from os.path import expanduser
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class TestApp(App):
    def build(self):
        label = BoxLayout()
        label.add_widget(Button(text='Notification', on_release=self.btnnotification))
        label.add_widget(Button(text='Message', on_release=self.btnmessage))
        label.add_widget(Button(text='Error', on_release=self.btnerror))
        label.add_widget(Button(text='Confirmation', on_release=self.btnConfirm))
        return label

    def btnnotification(self, *args):
        s_message = "here is the message text"
        Notification(
            text=s_message, show_time=3, size_hint=(0.8, 0.4),
            title='Results of the popup ( will disappear after 3 seconds ):')

    def btnmessage(self, *args):
        Message(text='It could be your Ad', title='Message demo')
    def btnerror(self, *args):
        Error(text='Don`t panic! Its just the Error demo.')
    def btnConfirm(self, *args):
        Confirmation(text='Do you see a confirmation?',
                          on_dismiss=self.my_callback)
        
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

        Notification(
            text=s_message, show_time=3, size_hint=(0.8, 0.4),
            title='Results of the popup ( will disappear after 3 seconds ):')


if __name__ == '__main__':
    TestApp().run()
