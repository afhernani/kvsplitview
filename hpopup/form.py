"""
Module form.py
==============

This module contains the base class for GUI forms. Also
subclasses which implement some simple forms.

Classes:

* Form: Base class for all the GUI forms.

* Slider: Represents :class:`~kivy.uix.slider.Slider` in popup.

* TextInput: Represents a single line TextInput in popup.

* Notes: Represents a multiline TextInput in popup.

* Authorization: Represents simple authorization form.


Form class
===========

Subclass of :class:`hpopup.HBase`.
The base class for all the GUI forms. Also you can use this class to create
your own forms. To do this you need to implement :meth:`Form._get_form` in
your subclass::

    class MyForm(Form):
        def _get_form(self):
            layout = BoxLayout()
            layout.add_widget(Label(text='Show must go'))
            layout.add_widget(Switch(id='main_switch'))
            return layout

    popup = MyForm(title='Party switch')

IMPORTANT: widgets, the values of which must be received after the close of
the form, must have an "id" attribute (see an example above). Current version
supports obtaining values of following widgets: TextInput, Switch, CheckBox,
Slider.

To obtain this values you need just use :meth:`Form.get_value`::

    def my_callback(instance):
        print('Switch value: ' + str(instance.get_value('main_switch')))

    popup = MyForm(title='Party switch', on_dismiss=my_callback)

If you omit an argument for the :meth:`Form.get_value`, method returns
a first value from the values dictionary. It is useful if the layout has only
one widget.

Another way to obtain values is :attr:`Form.values`::

    def my_callback(instance):
        print('Values: ' + str(instance.values))

    popup = MyForm(title='Party switch', on_dismiss=my_callback)

NOTE: The values are available only when the event `on_dismiss` was triggered.

.. versionadded:: 0.2.3
    You can set list of the required fields using following parameter::

        popup = Form(required_fields={
            'login': 'Login', 'password': 'Password'})

    Required fields checked when you press any button other than the "Cancel".


Slider class
=============

Subclass of :class:`hpopup.Form`.
Represents :class:`~kivy.uix.slider.Slider` in a popup. Properties
:attr:`Slider.value`, :attr:`Slider.min`, :attr:`Slider.max` and
:attr:`Slider.orientation` is binded to an appropriate properties of
the :class:`~kivy.uix.progressbar.lider`.

Also :class:`hpopup.Slider` has the event 'on_change'. You can bind
your callback to respond on the slider's position change.

Following example will create a :class:`popup.Slider` object::

    def my_callback(instance, value):
        print('Current volume level: %0.2f' % value)

    popup = Slider(title='Volume', on_change=my_callback)

Another example you can see in the demo app module.

.. versionadded:: 0.2.3
    You can display the slider's value in the title using following parameter::

        popup = Slider(title_template='Volume: %0.2f', on_change=my_callback)

    NOTE: Be careful and use the only one formatting operator.


Textinput and Notes classes
=============================

Subclasses of :class:`popup.Form`.
Both classes are represents :class:`~kivy.uix.textinput.TextInput` in a popup.
The difference is that the class :class:`hpopup.Textinput` is used to enter
one text line, and the class :class:`hpopup.Notes` - for multiline text.

Following example will create a :class:`~kivy.uix.textinput.TextInput` object
with the specified default text::

    def my_callback(instance):
        print('Your answer: ' + str(instance.get_value()))

    popup = Textinput(title='What`s your mood?',
                       text='I`m in the excellent mood!',
                       on_dismiss=my_callback)

NOTE: Pressing "Enter" key will simulate pressing "OK" on the popup. Valid for
the :class:`hpopup.Textinput` ONLY.

.. versionadded:: 0.2.3
    :class:`hpopup.Notes` allows you to specify a list of strings as the
    default value::

        def my_callback(instance):
            print('Edited text: ' + str(instance.lines))

        popup = Notes(lines=['1st row', '2nd row', '3rd row'],
                       on_dismiss=my_callback)


Authorization class
====================

Subclass of :class:`popup.Form`.
This class is represents a simple authorization form.
Use :attr:`hpopup.Authorization.login` and
:attr:`hpopup.Authorization.password` to set default values for the login and
password::

    def my_callback(instance):
        print('Auth values: ' + str(instance.values))

    Authorization(on_dismiss=my_callback, login='login', password='password')

Also, you can set a default value for the checkbox "Login automatically" via
:attr:`xpopup.XAuthorization.autologin`.


.. versionadded:: 0.2.3
    Set :attr:`hpopup.Authorization.autologin` to None - checkbox will be
    hidden.


To obtain the specific value, use following ids:

* login -  TextInput for the login

* password - TextInput for the password

* autologin - checkbox "Login automatically"

"""

from kivy import metrics
from kivy.factory import Factory
from kivy.properties import (NumericProperty, StringProperty, BooleanProperty,
    ListProperty, OptionProperty, DictProperty)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.slider import Slider
from kivy.uix.switch import Switch
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
try:
    from .hbase import HBase
    from .notification import Error
except:
    from hbase import HBase
    from notification import Error

__author__ = 'ophermit, hernai'
__all__ = ('HSlider', 'HTextInput', 'Notes', 'Authorization')


class Form(HBase):
    """Form class. See module documentation for more information.
    """

    buttons = ListProperty([HBase.BUTTON_OK, HBase.BUTTON_CANCEL])
    '''List of button names. Can be used when using custom button sets.

    :attr:`buttons` is a :class:`~kivy.properties.ListProperty` and defaults to
    [Base.BUTTON_OK, Base.BUTTON_CANCEL].
    '''

    values = DictProperty({})
    '''Dict of pairs <widget_id>: <widget_value>. Use it to get the data from
    form fields. Supported widget classes: TextInput, Switch, CheckBox, Slider.

    :attr:`values` is a :class:`~kivy.properties.DictProperty` and defaults to
    {}, read-only.
    '''

    required_fields = DictProperty({})
    '''Dict of pairs <widget_id>: <widget_title>. Use it to set required fields
    in the form. If found blank widget with <widget_id>, its <widget_title>
    appears in the error message. Supported widget classes: TextInput.

    .. versionadded:: 0.2.3

    :attr:`values` is a :class:`~kivy.properties.DictProperty` and defaults to
    {}.
    '''

    def __init__(self, **kwargs):
        self._ui_form_container = BoxLayout()
        super(Form, self).__init__(**kwargs)
        self._ui_form_container.add_widget(self._get_form())

    def _get_body(self):
        return self._ui_form_container

    def _on_click(self, instance):
        """Pre-dismiss method.
        Gathers widget values. Checks the required fields.
        Ignores it all if the "Cancel" was pressed.
        """
        instance_id = instance.text
        if instance_id != self.BUTTON_CANCEL:
            self.values = {}
            required_errors = []
            for widget in self._ui_form_container.walk(restrict=True):
                t_id = widget.__class__
                if t_id is not None:
                    if isinstance(widget, TextInput):
                        t_value = widget.text
                        if self.required_fields and\
                                t_id in self.required_fields.keys()\
                                and not t_value:
                            required_errors.append(self.required_fields[t_id])
                    elif isinstance(widget, Switch)\
                            or isinstance(widget, CheckBox):
                        t_value = widget.active
                    elif isinstance(widget, Slider):
                        t_value = widget.value
                    else:
                        t_value = 'Not supported: ' + widget.__class__.__name__

                    self.values[t_id] = t_value

            if required_errors:
                Error(text='Following fields are required:\n' + ', '.join(required_errors))
                return

        super(Form, self)._on_click(instance)

    def _get_form(self):
        raise NotImplementedError

    def get_value(self, ps_id=''):
        """Obtain values from the widgets on the form.

        :param ps_id: widget id (optional)
            If omit, method returns a first value from the values dictionary
        :return: value of widget with specified id
        """
        assert len(self.values) > 0
        if ps_id == '':
            return self.values.get(list(self.values.keys())[0])
        else:
            return self.values.get(ps_id)


class HSlider(Form):
    """HSlider class. See module documentation for more information.

    :Events:
        `on_change`:
            Fired when the :attr:`~kivy.uix.slider.Slider.value` is changed.
    """
    __events__ = ('on_change', )

    buttons = ListProperty([Form.BUTTON_CLOSE])
    '''Default button set for the popup
    '''

    min = NumericProperty(0.)
    max = NumericProperty(1.)
    value = NumericProperty(.5)
    orientation = OptionProperty(
        'horizontal', options=('vertical', 'horizontal'))
    '''Properties that are binded to the same slider properties.
    '''

    title_template = StringProperty('')
    '''Template for the formatted title. Use it if you want display the
    slider's value in the title. See module documentation for more information.

    .. versionadded:: 0.2.3

    :attr:`title_template` is a :class:`~kivy.properties.StringProperty` and
    defaults to ''.
    '''

    def __init__(self, **kwargs):
        super(HSlider, self).__init__(**kwargs)
        self._update_title()

    def _update_title(self):
        if self.title_template:
            self.title = self.title_template % self.value

    def _get_form(self):
        slider = Slider(min=self.min, max=self.max, value=self.value, orientation=self.orientation)
        setattr(slider, 'id', 'value')
        slider.bind(value=self.setter('value'))
        bind = self.bind
        bind(min=slider.setter('min'))
        bind(max=slider.setter('max'))
        bind(value=slider.setter('value'))
        bind(orientation=slider.setter('orientation'))
        return slider

    def on_value(self, instance, value):
        self._update_title()
        self.dispatch('on_change', value)

    def on_change(self, value):
        pass


class HTextInput(Form):
    """Textinput class. See module documentation for more information.
    """

    text = StringProperty('')
    '''This property represents default text for the TextInput.

    :attr:`text` is a :class:`~kivy.properties.StringProperty` and defaults to
    ''.
    '''

    def _get_form(self):
        layout = BoxLayout(orientation='vertical', spacing=5)
        text_input = TextInput(multiline=False, text=self.text,
                               on_text_validate=self._on_text_validate,
                               # DON`T UNCOMMENT OR FOUND AND FIX THE ISSUE
                               # if `focus` set to `True` - TextInput will be
                               # inactive to edit
                               # focus=True,
                               size_hint_y=None, height=metrics.dp(33))
        setattr(text_input, 'id', 'text')
        layout.add_widget(Widget())
        layout.add_widget(text_input)
        layout.add_widget(Widget())
        return layout

    def _on_text_validate(self, instance):
        button = Button(text=self.BUTTON_OK)
        setattr(button, 'id', self.BUTTON_OK )
        self._on_click(button)


class Notes(Form):
    """Notes class. See module documentation for more information.
    """

    size_hint_x = NumericProperty(.9, allownone=True)
    size_hint_y = NumericProperty(.9, allownone=True)
    '''Default size properties for the popup
    '''

    text = StringProperty('')
    '''This property represents default text for the TextInput.

    :attr:`text` is a :class:`~kivy.properties.StringProperty` and defaults to
    ''.
    '''

    lines = ListProperty()
    '''This property represents default text for the TextInput as list of
    strings.

    .. versionadded:: 0.2.3

    :attr:`lines` is a :class:`~kivy.properties.ListProperty` and defaults to
    [].
    '''

    def _get_form(self):
        t = self.text
        if self.lines:
            t = '\n'.join(self.lines)
        res = TextInput(text=t)
        setattr(res, 'id', 'text')
        return res #TextInput(id='text', text=t)

    def _on_click(self, instance):
        if instance.text != self.BUTTON_CANCEL:
            for widget in self._ui_form_container.walk(restrict=True):
                if isinstance(widget, TextInput):
                    self.lines = widget.text.split('\n')

        super(Form, self)._on_click(instance)


class Authorization(Form):
    """Authorization class. See module documentation for more information.
    """
    BUTTON_LOGIN = 'Login'

    login = StringProperty(u'')
    '''This property represents default text in the `login` TextInput.
    For initialization only.

    :attr:`login` is a :class:`~kivy.properties.StringProperty` and defaults to
    ''.
    '''

    password = StringProperty(u'')
    '''This property represents default text in the `password` TextInput.
    For initialization only.

    :attr:`password` is a :class:`~kivy.properties.StringProperty` and defaults
    to ''.
    '''

    autologin = BooleanProperty(False, allownone=True)
    '''This property represents default value for the CheckBox
    "Login automatically". For initialization only.

    .. versionadded:: 0.2.3

        If None - checkbox is hidden.

    :attr:`autologin` is a :class:`~kivy.properties.BooleanProperty` and
    defaults to False.
    '''

    title = StringProperty('Authorization')
    '''Default title for the popup
    '''

    buttons = ListProperty([BUTTON_LOGIN, Form.BUTTON_CANCEL])
    '''Default button set for the popup
    '''

    size_hint_x = NumericProperty(None, allownone=True)
    size_hint_y = NumericProperty(None, allownone=True)
    width = NumericProperty(metrics.dp(350))
    height = NumericProperty(metrics.dp(200))
    '''Default size properties for the popup
    '''

    def _get_form(self):
        layout = BoxLayout(orientation='vertical', spacing=5)
        layout.add_widget(Widget())

        pnl = BoxLayout(size_hint_y=None, height=metrics.dp(28), spacing=5)
        pnl.add_widget(
            Label(text='Login:', halign='right',
                           size_hint_x=None, width=metrics.dp(80)))
        text_input = TextInput(multiline=False,
                                 font_size=metrics.sp(14), text=self.login)
        setattr(text_input, 'id', 'login')
        pnl.add_widget(text_input)
        layout.add_widget(pnl)

        pnl = BoxLayout(size_hint_y=None, height=metrics.dp(28), spacing=5)
        pnl.add_widget(
            Label(text='Password:', halign='right',
                           size_hint_x=None, width=metrics.dp(80)))
        text_password = TextInput(multiline=False, font_size=14,
                                 password=True, text=self.password)
        setattr(text_password, 'id', 'password')
        pnl.add_widget(text_password)
        layout.add_widget(pnl)

        if self.autologin is not None:
            pnl = BoxLayout(size_hint_y=None, height=metrics.dp(28), spacing=5)
            checkbox = CheckBox(
                size_hint_x=None, width=metrics.dp(80),
                active=self.autologin)
            setattr(checkbox, 'id', 'autologin')
            pnl.add_widget(checkbox)
            pnl.add_widget(
                Label(text='Login automatically', halign='left'))
            layout.add_widget(pnl)

        layout.add_widget(Widget())
        return layout


#### comprobaciones. #######################

from os.path import expanduser
from kivy.app import App
from kivy.logger import Logger
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class TestApp(App):
    def build(self):
        label = BoxLayout()
        label.add_widget(Button(text='Slider', on_release=self.btnSlider))
        label.add_widget(Button(text='HTextInput', on_release=self.btnTextinput))
        label.add_widget(Button(text='Notes', on_release=self.btnNotes))
        label.add_widget(Button(text='Autoritation', on_release=self.btnAuto))
        return label

    def btnSlider(self, *args):
        self._o_popup = HSlider(
                min=.4, max=.9, value=.5, size_hint=(.6, .5),
                title_template='Slider test, Value: %0.2f',
                buttons=['Horizontal', 'Vertical', 'Close'],
                on_change=self._slider_value, on_dismiss=self._slider_click)

    @staticmethod
    def _slider_value(instance, value):
        if instance.orientation == 'vertical':
            instance.size_hint_x = value
        else:
            instance.size_hint_y = value

    @staticmethod
    def _slider_click(instance):
        if instance.button_pressed == 'Horizontal':
            instance.orientation = 'horizontal'
            instance.size_hint = (.6, .5)
            instance.min = .4
            instance.max = .9
            instance.value = .5
            return True
        elif instance.button_pressed == 'Vertical':
            instance.orientation = 'vertical'
            instance.size_hint = (.5, .6)
            instance.min = .4
            instance.max = .9
            instance.value = .5
            return True

    def btnTextinput(self, *agrs):
        HTextInput(title='Edit text', text='I\'m a text',
                       on_dismiss=self.my_callback)

    def my_callback(self, instance):
        if instance.is_canceled():
            return

        s_message = 'Pressed button: %s\n\n' % instance.button_pressed

        '''try:
            values = instance.values
            for kw in values:
                s_message += ('<' + kw + '> : ' + str(values[kw]) + '\n')
        except AttributeError:
            pass '''

        Logger.info(msg=s_message)
    
    def btnNotes(self, *args):
        Notes(title='Edit notes', on_dismiss=self._callback_notes,
                   lines=['Text', 'Too many text...', 'Yet another row.'])

    # @staticmethod
    def _callback_notes(self, instance):
        if instance.is_canceled():
            return

        s_message = 'Pressed button: %s\n\n' % instance.button_pressed
        s_message += str(instance.lines)
        Logger.warning(msg=s_message)
        from notification import Notification
        Notification(
            text=s_message, show_time=3, size_hint=(0.8, 0.4),
            title='Notes demo ( will disappear after 3 seconds ):')

    def btnAuto(self, *args):
        Authorization(
                on_dismiss=self.my_callback, login='login',
                required_fields={'login': 'Login', 'password': 'Password'},
                password='password')

if __name__ == '__main__':
    TestApp().run()