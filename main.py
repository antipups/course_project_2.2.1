from kivy.animation import Animation
import ctypes
from kivy.config import Config
from kivy.uix.scrollview import ScrollView

Config.set('graphics', 'width', 300)
Config.set('graphics', 'height', 175)
Config.set('graphics', 'resizable', 0)
from kivy.uix.actionbar import ActionBar, ActionView, ActionItem, ActionButton
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
import datetime
import os
import re
import threading
import time
from functools import partial
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
import util
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner


class FloatInput(TextInput):
    pat = re.compile('[^(0-9)(a-z)(A-Z)]')

    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join([re.sub(pat, '', s) for s in substring.split('.', 1)])
        return super(FloatInput, self).insert_text(s, from_undo=from_undo)


class MyApp(App):

    def build(self):
        """
            Создание окна авторизации
        :return:
        """

        self.title = 'Авторизация'

        sm = ScreenManager()
        log = Screen(name='login')
        reg = Screen(name='regist')
        sm.add_widget(log)
        sm.add_widget(reg)

        bl = BoxLayout(orientation='vertical')
        bl.add_widget(Label(text='Авторизация'))
        login = FloatInput(hint_text='Логин',
                           id='login')
        bl.add_widget(login)
        password = FloatInput(hint_text='Пароль',
                              id='password')
        bl.add_widget(password)

        bl_mode = BoxLayout(orientation='horizontal')
        bl_mode.add_widget(Button(text='Зарегистрироватся',
                                  on_press=lambda x: sm.switch_to(reg, direction='left')))
        bl_mode.add_widget(Button(text='Войти',
                                  on_press=lambda x: self.auth_in(login, password)))
        bl.add_widget(bl_mode)
        log.add_widget(bl)

        bl_reg = BoxLayout(orientation='vertical')
        bl_reg.add_widget(Label(text='Регистрация'))

        reg_login = FloatInput(hint_text='Логин',
                               id='login')
        bl_reg.add_widget(reg_login)
        reg_password = FloatInput(hint_text='Пароль',
                                  id='password')
        bl_reg.add_widget(reg_password)

        bl_mode_reg = BoxLayout(orientation='horizontal')
        bl_mode_reg.add_widget(Button(text='Зарегистрироватся',
                                      on_press=lambda x: sm.switch_to(log) if self.reg_in(reg_login, reg_password) else sm.switch_to(reg)))
        bl_mode_reg.add_widget(Button(text='Отмена',
                                      on_press=lambda x: sm.switch_to(log, direction='right')))
        bl_reg.add_widget(bl_mode_reg)
        reg.add_widget(bl_reg)

        Window.add_widget(sm)

    def reg_in(self, login_widget, password_widget):
        """
            Регистрация пользователя
        :param instance:
        :return:
        """
        if util.reg_user(login_widget.text, password_widget.text):
            login_widget.background_color = password_widget.background_color = (0, 1, 0, 1)
            Clock.schedule_once(partial(self.decolor, login_widget, password_widget, 0, 'green'))
        else:
            login_widget.background_color = password_widget.background_color = (1, 0, 0, 1)
            Clock.schedule_once(partial(self.decolor, login_widget, password_widget, 0, 'red'))
        login_widget.text = password_widget.text = ''

    def auth_in(self, login_widget, password_widget):
        """
            Проверка ввода логина и пароля
        :param instance:
        :return:
        """
        if util.has_user(login_widget.text, password_widget.text):
            for auth_wind in Window.children:
                Window.remove_widget(auth_wind)
            Clock.schedule_once(partial(self.anim_main_menu, 300, 175), 0.1)
        else:
            login_widget.background_color = password_widget.background_color = (1, 0, 0, 1)
            login_widget.text = password_widget.text = ''
            Clock.schedule_once(partial(self.decolor, login_widget, password_widget, 0, 'red'))

    def decolor(self, login_widget, password_widget, visible, color, times):
        """
        Анимация красного цвета при неверном вводе пароля
        :param login_widget:        виджет логина
        :param password_widget:     виджет пароля
        :param visible:             видимость, прибавляется по 0.1
        :param times:
        :return:
        """
        if visible < 1:
            password_widget.background_color = login_widget.background_color = (visible, 1, visible, 1) if color == 'green' else (1, visible, visible, 1)
            visible += .1
            Clock.schedule_once(partial(self.decolor, login_widget, password_widget, visible, color), 0.05)

    def anim_main_menu(self, width, height, times):
        """
            Анимация изменения размера для главного окна
        :param width:
        :param height:
        :param times:
        :return:
        """
        if width < 600:
            width += 50 / 6
            height += 69 / 6
            Window.top = Window.top - 42.85 / 10
            Window.left = Window.left - 47.85 / 12
            Window.size = (width, height)
            Clock.schedule_once(partial(self.anim_main_menu, width, height), 0.0005)
        else:
            Window.size = (width, 600)
            self.main_menu()

    def main_menu(self):
        """
                Функция в которой прорисоваваются все главные элементы управления,
            главное меню.
        :return:
        """
        self.title = 'Главное меню'
        sm = ScreenManager()
        main_screen = Screen()
        sm.add_widget(main_screen)
        sm.switch_to(main_screen)

        bl = BoxLayout(orientation='vertical')

        bl_header = BoxLayout(orientation='horizontal',
                              size_hint_y=None,
                              height=50)

        spinner = Spinner(
            # default value shown
            text='Таблицы',
            # available values
            values=('Типы привилегий', 'Город', 'Страна', 'Соц. положение', 'Районы',
                    'Льгота', 'Тариф', 'Абонент', 'АТС', 'Звонок'),
        )

        table = GridLayout(row_default_height=50,
                           row_force_default=True,
                           size_hint_y=None)
        table.bind(minimum_height=table.setter('height'))
        scroll = ScrollView(size_hint=(1, None), size=(Window.width, 550))
        scroll.add_widget(table)

        def show_selected_value(spinner, text):

            table.clear_widgets()
            dict_of_data = util.read_tables(text)
            print(dict_of_data)
            table.cols = len(dict_of_data)

            for key in dict_of_data.keys():
                table.add_widget(Button(text=key,
                                        height=50,
                                        size_hint_y=None))

            for row in zip(*dict_of_data.values()):
                for element in row:
                    table.add_widget(Button(text=str(element)))

        spinner.bind(text=show_selected_value)
        # выбор чего-то

        bl_header.add_widget(spinner)
        bl_header.add_widget(Button(text='Запросы'))
        bl.add_widget(bl_header)

        bl.add_widget(scroll)

        main_screen.add_widget(bl)
        Window.add_widget(sm)

        # вывод всего меню, и создание экранов



if __name__ == '__main__':
    MyApp().run()