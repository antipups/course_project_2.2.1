import functools

from kivy.animation import Animation
import ctypes
from kivy.config import Config
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
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
        if width < 1200:
            width += 100 / 6
            height += 50 / 6
            Window.top = Window.top - 42.85 / 10
            Window.left = Window.left - 94 / 12
            Window.size = (width, height)
            Clock.schedule_once(partial(self.anim_main_menu, width, height), 0.00005)
        else:
            Window.size = (width, 600)
            self.main_menu()

    def switch(self, screen, direction):
        """
            Переключалка экранов
        """
        self.sm.transition.direction = direction
        self.sm.current = screen

    def main_menu(self):
        """
                Функция в которой прорисоваваются все главные элементы управления,
            главное меню.
        :return:
        """
        self.title = 'Главное меню'
        self.sm = ScreenManager()
        main_screen = Screen(name='main')
        self.sm.add_widget(main_screen)
        self.sm.add_widget(self.modification_table())
        self.sm.switch_to(main_screen)

        bl = BoxLayout(orientation='vertical')

        bl_header = BoxLayout(orientation='horizontal',
                              size_hint_y=None,
                              height=50)

        spinner = Spinner(
            text='Вывод таблицы',
            values=util.name_of_table_on_rus,
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

        def switch_to_mode(instance):
            self.sm.transition.direction = 'left'
            self.sm.current = 'mode'

        bl_header.add_widget(Button(text='Модификация таблиц',
                                    on_press=switch_to_mode))
        bl_header.add_widget(Button(text='Запросы'))
        bl.add_widget(bl_header)

        bl.add_widget(scroll)

        main_screen.add_widget(bl)
        Window.add_widget(self.sm)

    def modification_table(self):
        """
            Экран модификации данных в таблицах
        :return:
        """
        mode_screen = Screen(name='mode')
        bl = BoxLayout(orientation='vertical')
        mode_screen.add_widget(bl)

        # создание экрана и добавление в него главного лайаута

        spiner = Spinner(text='Выберите таблицу для редактирования',
                         values=util.name_of_table_on_rus,
                         disabled=True,
                         height=50,
                         size_hint_y=None)
        bl.add_widget(spiner)

        # создание лайаута на вывод режимов
        bl_modes = BoxLayout(orientation='horizontal',
                             size_hint_y=None,
                             height=50)

        # создание лайаута для полей ввода
        gl = GridLayout(size_hint_y=None,
                        row_default_height=50,
                        row_force_default=True)
        gl.bind(minimum_height=gl.setter('height'))
        scroll = ScrollView(size_hint=(1, None), size=(Window.width, Window.height -150))
        scroll.add_widget(gl)

        # создание лайаута для вывода лейблов (что вводить?)
        bl_title_of_rows = BoxLayout(orientation='horizontal',
                                     size_hint_y=None,
                                     height=50)

        bl.add_widget(bl_title_of_rows)
        bl.add_widget(scroll)
        bl.add_widget(bl_modes)

        dict_of_modes = ('Добавить', 'Изменить', 'Удалить', 'Найти')

        list_of_rows = []

        def action(instance):
            """
                При нажатии на кнопку какого-либо мода, двойное удаление и прочее прочее
            :param instance:
            :return:
            """
            for widget in bl_modes.children[1:]:
                if widget.background_color == [0, 1, 1, 1] and widget.text == 'Удалить' and widget == instance:

                    if len(list_of_rows) > 1:
                        """
                            Если нажали на таблицу и выбрали записи на удаление
                        """
                        temp = BoxLayout(orientation='vertical')

                        def yes(instance):
                            util.delete(list_of_rows[0], list_of_rows[1:])
                            widgets_on_remove = []
                            for widget in gl.children[::-1]:
                                if widget.id in list_of_rows[1:]:
                                    widgets_on_remove.append(widget)
                            else:
                                for widget in widgets_on_remove:
                                    gl.remove_widget(widget)
                            del list_of_rows[1:]
                            popup.dismiss()

                        temp.add_widget(Label(text='Вы уверены что хотите удалить выбранные записи?'))
                        temp.add_widget(Button(text='Да',
                                               on_press=yes,
                                               size_hint_y=None,
                                               height=35, ))
                        temp.add_widget(Button(text='Нет',
                                               size_hint_y=None,
                                               height=35,
                                               on_press=lambda x: popup.dismiss()))
                        popup = Popup(title='Подтверждение удаления',
                                      size_hint=(None, None),
                                      size=(400, 400),
                                      content=temp)
                        popup.open()
                        break
                    elif len(list_of_rows) == 1:
                        """
                            Если нажали на удалить и не выбрали ЗАПИСЬ
                        """
                        temp = BoxLayout(orientation='vertical')
                        engl, rus = util.get_fields_add(list_of_rows[0])
                        for column in engl:
                            widget = None
                            if column.startswith('id_of_'):
                                widget = Spinner(text='--- Выберите ---',
                                                 values=util.get_mini_table(column[6:]), )
                            else:
                                widget = TextInput(hint_text=rus[engl.index(column)])
                            widget.id = column
                            widget.size_hint_y = None
                            widget.height = 35
                            temp.add_widget(widget)
                        else:
                            temp.add_widget(Widget())

                            button_layout = BoxLayout(orientation='horizontal')
                            button_layout.add_widget(Button(text='Отмена',
                                                            on_press=lambda x: popup.dismiss(),
                                                            size_hint_y=None,
                                                            height=35))

                            def delete(instance):
                                dict_of_data = {}
                                for widget in temp.children[2:]:
                                    if widget.text and widget.text.find('---') == -1:
                                        dict_of_data.update({widget.id: widget.text if widget.text.find(
                                            '|') == -1 else widget.text[:widget.text.find(' |')]})
                                else:
                                    if len(dict_of_data) > 0:
                                        widgets_on_remove = []
                                        pop_elements = util.delete_on_row(list_of_rows[0], dict_of_data)
                                        for widget in gl.children:
                                            if int(widget.id) in pop_elements:
                                                widgets_on_remove.append(widget)
                                        for widget in widgets_on_remove:
                                            gl.remove_widget(widget)

                            button_layout.add_widget(Button(text='Удалить',
                                                            on_press=delete,
                                                            size_hint_y=None,
                                                            height=35))

                            temp.add_widget(button_layout)

                        popup = Popup(title='Удаление через поля',
                                      size_hint=(None, None),
                                      size=(400, 400),
                                      content=temp)
                        popup.open()
                        break
                    else:
                        """
                            Если нажали на удалить и не выбрали ТАБЛИЦУ
                        """
                        temp = BoxLayout(orientation='vertical')
                        temp.add_widget(Label(text='Сначала выберите таблицу!!!'))
                        temp.add_widget(Button(text='Хорошо',
                                               on_press=lambda x: popup.dismiss(),
                                               size_hint_y=None,
                                               height=35))
                        popup = Popup(title='Предупреждение',
                                      size_hint=(None, None),
                                      size=(400, 400),
                                      content=temp)
                        popup.open()
                        break

                else:
                    widget.background_color = (0, 1, 0, 1)
            else:
                spiner.text = 'Выберите таблицу для редактирования'
                bl_title_of_rows.clear_widgets()
                gl.clear_widgets()

            spiner.disabled = False
            instance.background_color = (0, 1, 1, 1)

        for title_of_mode in dict_of_modes:
            bl_modes.add_widget(Button(text=title_of_mode,
                                       background_color=(0, 1, 0, 1),
                                       on_press=action))
        else:
            bl_modes.add_widget(Button(text='Назад',
                                       background_color=(1, 0, 0, 1),
                                       on_press=lambda x: self.switch('main', 'right')))

        def show_selected_value(spinner, text):
            """
                При нажатии на таблицу, генерируем в зависимости от режима записи.
            :param spinner:
            :param text:
            :return:
            """
            bl_title_of_rows.clear_widgets()
            gl.clear_widgets()
            list_of_rows.clear()
            list_of_rows.append(text)
            mode = None
            for widget in bl_modes.children:
                if widget.background_color == [0, 1, 1, 1]:
                    mode = widget.text
                    break

            if mode == 'Добавить':
                """
                    Добавление в БД.
                """
                bl_title_of_rows.height = 50
                engl, rus = util.get_fields_add(text)
                gl.cols = len(engl)
                for title in rus:
                    bl_title_of_rows.add_widget(Button(text=title,
                                                       size_hint_y=None,
                                                       height=50,
                                                       background_color=(0, 1, 0, 1),))

                for column in engl:
                    widget = None
                    if column.startswith('id_of_'):
                        widget = Spinner(text='--- Выберите ---',
                                         values=util.get_mini_table(column[6:]),)
                    else:
                        widget = TextInput()
                    widget.id = column
                    widget.size_hint_y = None
                    widget.height = 50
                    gl.add_widget(widget)
                else:
                    def add(instance):
                        dict_of_data = {}
                        instance.background_color, instance.text = (1, 1, 1, 1), 'Добавить'
                        for widget in reversed(gl.children[1:]):
                            if widget.text and widget.text.find('---') == -1:
                                widget.background_color = (1, 1, 1, 1)
                                dict_of_data.update({widget.id: widget.text if widget.text.find('|') == -1 else widget.text[:widget.text.find(' |')]})
                            else:
                                instance.background_color = widget.background_color = (1, 0, 0, 1)
                                return
                        result = util.add(text, dict_of_data)
                        if not result[0] and len(result) == 3:
                            for widget in reversed(gl.children[1:]):
                                if widget.id == result[1]:
                                    widget.text, widget.hint_text, widget.hint_text_color = '', result[2], (1, 0, 0, 1)
                                else:
                                    widget.hint_text_color = (1, 1, 1, 1)
                        else:
                            instance.background_color = (0, 1, 0, 1) if result[0] else (1, 0, 0, 1)
                            instance.text = result[1]

                    gl.add_widget(Button(text='Добавить',
                                         on_press=add,
                                         size_hint_y=None,
                                         height=50))
                    gl.add_widget(Widget())

            elif mode == 'Удалить':
                """
                    Удаление из бд
                """
                bl_title_of_rows.clear_widgets()
                gl.clear_widgets()
                table = gl
                dict_of_data = util.read_tables(text)
                table.cols = len(dict_of_data)

                for key in dict_of_data.keys():
                    bl_title_of_rows.add_widget(Button(text=key,
                                                       height=50,
                                                       size_hint_y=None,
                                                       background_color=(0, 1, 0, 1)))

                def action_on_db(instance):
                    if not instance.id in list_of_rows:
                        list_of_rows.append(instance.id)
                        for widget in gl.children:
                            if widget.id == instance.id:
                                widget.background_color = (0, 1, 1, .5)
                    else:
                        list_of_rows.remove(instance.id)
                        for widget in reversed(gl.children):
                            if widget.id == instance.id:
                                widget.background_color = (1, 1, 1, 1)

                for row in zip(*dict_of_data.values()):
                    id_of_row = row[0]
                    for element in row:
                        table.add_widget(Button(text=str(element),
                                                id=str(id_of_row),
                                                on_press=action_on_db))

        spiner.bind(text=show_selected_value)
        # bl.add_widget(Widget())
        return mode_screen


if __name__ == '__main__':
    MyApp().run()