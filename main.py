import functools
import random

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
        self.title = 'Курсовой проект'
        self.sm = ScreenManager()
        main_screen = Screen(name='main')
        self.sm.add_widget(main_screen)
        self.sm.add_widget(self.modification_table())
        self.sm.add_widget(self.query_screen())
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
            if text.startswith('Таблица'):
                return
            table.clear_widgets()
            dict_of_data = util.read_tables(text)
            table.cols = len(dict_of_data)

            for key in dict_of_data.keys():
                table.add_widget(Button(text=key,
                                        height=50,
                                        size_hint_y=None,
                                        background_color=(0, 1, 0, 1)))

            counter = 0
            for row in zip(*dict_of_data.values()):
                counter += 1
                if text == 'Город' and counter > 100:
                    continue
                for element in row:
                    table.add_widget(Button(text=str(element)))

            spinner.text = 'Таблица - ' + text + '; Кол-во записей - ' + str(counter)

        spinner.bind(text=show_selected_value)
        # выбор чего-то

        bl_header.add_widget(spinner)

        def switch_to_mode(instance):
            self.sm.transition.direction = 'left'
            self.sm.current = 'mode'

        def switch_to_query(instance):
            self.sm.transition.direction = 'right'
            self.sm.current = 'query'

        bl_header.add_widget(Button(text='Модификация таблиц',
                                    on_press=switch_to_mode))
        bl_header.add_widget(Button(text='Запросы',
                                    on_press=switch_to_query))
        bl.add_widget(bl_header)

        bl.add_widget(scroll)

        main_screen.add_widget(bl)
        Window.add_widget(self.sm)

    def popup_for_delete_rows(self, gl, list_of_rows):
        """
            Генерируем запрос на удаление и форму предупреждения на удаление.
        :param gl:
        :param list_of_rows:
        :return:
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

    def popup_for_delete_on_fields(self, gl, list_of_rows):
        """
            Удаление по выбранным пользователем полям
        :param gl:
        :param list_of_rows:
        :return:
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

    def popup_attention(self):
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

    def popup_for_update_rows(self, gl, list_of_rows):
        """
            Изменение выбранных строк
        :param gl:
        :param list_of_rows:
        :return:
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

            def update(instance):
                dict_of_old_data = {'id': []}
                for widget in gl.children:
                    if widget.background_color == [0, 1, 1, 0.5]:
                        if widget.id not in dict_of_old_data.get('id'):
                            dict_of_old_data.get('id').append(widget.id)

                dict_of_data = {}
                for widget in temp.children[2:]:
                    if widget.text and widget.text.find('---') == -1:
                        dict_of_data.update({widget.id: widget.text if widget.text.find('|') == -1 else widget.text[:widget.text.find(' |')]})
                else:
                    if len(dict_of_data) > 0:
                        pop_elements = util.update(list_of_rows[0], dict_of_old_data, dict_of_data)
                        if not pop_elements[0]:
                            instance.background_color = (1, 0, 0, 1)
                            if len(pop_elements) > 1:
                                for widget in temp.children:
                                    if widget.id == pop_elements[1]:
                                        widget.text = ''
                                        widget.hint_text_color = (1, 0, 0, 1)
                                        widget.hint_text = pop_elements[-1]
                                        break
                            return
                        else:
                            instance.background_color = (0, 1, 0, 1)
                            gl.clear_widgets()
                            table = gl
                            dict_of_data = util.read_tables(list_of_rows[0])
                            table.cols = len(dict_of_data)

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

            button_layout.add_widget(Button(text='Изменить',
                                            on_press=update,
                                            size_hint_y=None,
                                            height=35))

            temp.add_widget(button_layout)

        popup = Popup(title='Новые поля',
                      size_hint=(None, None),
                      size=(400, 400),
                      content=temp)
        popup.open()

    def popup_for_update_on_fields(self, gl, list_of_rows):
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

            dict_of_old_data = {}

            def update(instance):
                if instance.background_color == [1, 1, 1, 1] or instance.background_color == [1, 0, 0, 1]:
                    dict_of_old_data.clear()
                    for widget in temp.children[2:]:
                        if widget.text and widget.text.find('---') == -1:
                            dict_of_old_data.update({widget.id: widget.text if widget.text.find('|') == -1 else widget.text[:widget.text.find(' |')]})
                    else:
                        if len(dict_of_old_data) > 0:
                            result = util.check_row(list_of_rows[0], dict_of_old_data)
                            if result:
                                instance.background_color = (0, 1, 1, 1)
                                popup.title = 'Введите новые значения записей'
                            else:
                                instance.background_color = (1, 0, 0, 1)
                                popup.title = 'Не найденно существующих записей'
                else:
                    dict_of_new_data = {}
                    for widget in temp.children[2:]:
                        if widget.text and widget.text.find('---') == -1:
                            dict_of_new_data.update({widget.id: widget.text if widget.text.find('|') == -1 else widget.text[:widget.text.find(' |')]})
                    else:
                        if len(dict_of_new_data) > 0:
                            result = util.update_rows(list_of_rows[0], dict_of_old_data, dict_of_new_data)
                            if not result[0]:
                                instance.background_color = (0, 1, 1, 1)
                                if len(result) > 1:
                                    for widget in temp.children:
                                        if widget.id == result[1]:
                                            widget.text = ''
                                            widget.hint_text_color = (1, 0, 0, 1)
                                            widget.hint_text = result[-1]
                                            break
                                    return
                            popup.dismiss()
                            gl.clear_widgets()
                            table = gl
                            dict_of_data = util.read_tables(list_of_rows[0])
                            table.cols = len(dict_of_data)

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

            button_layout.add_widget(Button(text='Изменить',
                                            on_press=update,
                                            size_hint_y=None,
                                            height=35))

            temp.add_widget(button_layout)

        popup = Popup(title='Введите поля по которым будет редактирование',
                      size_hint=(None, None),
                      size=(400, 400),
                      content=temp)
        popup.open()

    def find_row(self, gl, list_of_row, amount_fields):
        name_of_table = list_of_row[0]
        dict_of_data = {}
        widgets_in_trash = []
        for widget in gl.children[:-amount_fields]:
            widgets_in_trash.append(widget)
        else:
            for widget in widgets_in_trash:
                gl.remove_widget(widget)

        for widget in gl.children[-amount_fields:]:
            if widget.text and widget.text.find('---') == -1:
                dict_of_data.update({widget.id: widget.text if widget.text.find('|') == -1 else widget.text[:widget.text.find(' |')]})
        else:
            result = util.find(name_of_table, dict_of_data)
            if not result[1]:
                return
            for row in zip(*result[0].values()):
                if row[0] not in result[1]:
                    continue
                for element in row[1:]:
                    gl.add_widget(Button(text=str(element),))

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
                    if widget.background_color == [0, 1, 1, 1] and widget.text in ('Удалить', 'Изменить') and widget == instance:
                        """
                            При повторном нажатии на кнопку, есть 3 состояния, записи выбраны, не выбраны, и не выбрана таблицы
                            при невыбранной таблице предупреждаем пользователя о выборе таблицы,
                            при невыбранной строчке даем пользователю форму по удалению / изменению по полю,
                            при выбранной строке удаляем / изменяем выбранные строки
                        """
                        if len(list_of_rows) > 1:
                            """
                                Если нажали на таблицу и выбрали записи на удаление / изменение
                            """
                            self.popup_for_delete_rows(gl, list_of_rows) if instance.text == 'Удалить' else self.popup_for_update_rows(gl, list_of_rows)
                            break
                        elif len(list_of_rows) == 1 and list_of_rows[0] != 'Выберите таблицу для редактирования':
                            """
                                Если нажали на удалить / изменить и не выбрали ЗАПИСЬ
                            """
                            self.popup_for_delete_on_fields(gl, list_of_rows) if instance.text == 'Удалить' else self.popup_for_update_on_fields(gl, list_of_rows)
                            break
                        else:
                            """
                                Если нажали на удалить и не выбрали ТАБЛИЦУ
                            """
                            self.popup_attention()
                            break

                    if widget.background_color == [0, 1, 1, 1] and widget.text == 'Найти' and widget == instance:
                        if len(list_of_rows) > 0:
                            self.find_row(gl, list_of_rows, len(bl_title_of_rows.children))
                            widget.background_color = (0, 1, 1, 1)
                        else:
                            self.popup_attention()
                        break
                    else:
                        widget.background_color = (0, 1, 0, 1)
                else:
                    """
                        Если сюда зашли, то есть цикл успешно завершился,
                        то это просто смена режима и мы сбрасываем все таблицы и данные
                    """
                    list_of_rows.clear()
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
                if text == 'Выберите таблицу для редактирования':
                    return
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

                elif mode in ('Удалить', 'Изменить'):
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
                elif mode == 'Найти':
                    bl_title_of_rows.height = 50
                    engl, rus = util.get_fields_add(text)
                    gl.cols = len(engl)
                    for title in rus:
                        bl_title_of_rows.add_widget(Button(text=title,
                                                           size_hint_y=None,
                                                           height=50,
                                                           background_color=(0, 1, 0, 1), ))

                    for column in engl:
                        widget = None
                        if column.startswith('id_of_'):
                            widget = Spinner(text='--- Выберите ---',
                                             values=util.get_mini_table(column[6:]), )
                        else:
                            widget = TextInput()
                        widget.id = column
                        widget.size_hint_y = None
                        widget.height = 50
                        gl.add_widget(widget)

            spiner.bind(text=show_selected_value)
            return mode_screen

    def query_screen(self):
        screen = Screen(name='query')
        main_bl = BoxLayout(orientation='horizontal')

        spinner = Spinner(text='Выберите запрос или действие',
                          values=['Вывести все Льготы по указанному типу',
                                  'Вывести все Звонки по городу и дате',
                                  'Вывести самый длинный звонок в\nгороде и в определенный день',
                                  'Вывести все АТС в заданному районе',
                                  'Вывести всех Абонентов по статусу',
                                  'Получение всех звонков по\nопределенному городу до опреде-\nлённого числа',
                                  'Получение звонков выше\nопределенной стоимости',
                                  'Получение количества звон-\nков по определенной АТС',
                                  'Получение самого длинного\nзвонка по определенной АТС',
                                  'Кто чаще пользуется услугами АТС',
                                  'Назад'],
                          size_hint=(None, None),
                          size=(300, 50))

        def selected_item(spinner, text):
            """
                Текст - это выбора запроса,
                table - это правая панель
            :param spinner:
            :param text:
            :return:
            """
            if text == 'Выберите запрос или действие':
                return
            if text == 'Назад':
                self.switch('main', 'left')
                return
            func_ = {'Вывести все Льготы по указанному типу': self.first_query,
                     'Вывести все Звонки по городу и дате': self.second_query,
                     'Вывести самый длинный звонок в\nгороде и в определенный день': self.third_query,
                     'Вывести все АТС в заданному районе': self.fourth_query,
                     'Вывести всех Абонентов по статусу': self.fifth_query,
                     'Получение всех звонков по\nопределенному городу до опреде-\nлённого числа': self.sixth_query,
                     'Получение звонков выше\nопределенной стоимости': self.seventh_query,
                     'Получение количества звон-\nков по определенной АТС': self.eight_query,
                     'Получение самого длинного\nзвонка по определенной АТС': self.ninth_query,
                     'Кто чаще пользуется услугами АТС': self.task1,
                     }.get(text)
            table.clear_widgets()
            func_(table)
            title_of_query.text = text
            spinner.text = 'Выберите запрос или действие'

        # всё до конца функции это генерация рабочего пространства, правая панель это table
        spinner.bind(text=selected_item)
        temp_bl = BoxLayout(orientation='vertical',
                            size_hint_x=None,
                            width=300)
        temp_bl.add_widget(spinner)
        title_of_query = Label(size_hint_y=None,
                               height=100)
        temp_bl.add_widget(title_of_query)
        temp_bl.add_widget(Widget())
        main_bl.add_widget(temp_bl)

        table = GridLayout(row_default_height=50,
                           row_force_default=True,
                           size_hint_y=None)
        table.bind(minimum_height=table.setter('height'))
        scroll = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        scroll.add_widget(table)
        main_bl.add_widget(scroll)
        screen.add_widget(main_bl)

        return screen

    def first_query(self, gl):
        """
            Первый запрос внутренне симмистричный на получение Льгот через их типы
        :param gl:
        :return:
        """
        def get_data_from_db(instance):
            """
            Формируем результат после нажатия в Попапе Готово
            :param instance:
            :return:
            """
            type_ = str()
            for widget in temp.children:
                if widget.id == 'spinner' and widget.text.find('---') == -1:
                    type_ = widget.text
                    break
            else:
                instance.background_color = (1, 0, 0, 1)
                return

            exsists_elements = util.first_query(type_[:type_.find(' | ')])
            dict_of_data = util.read_tables('Льгота')
            gl.cols = len(dict_of_data)

            for key in dict_of_data.keys():
                gl.add_widget(Button(text=key,
                                     height=50,
                                     size_hint_y=None,
                                     background_color=(0, 1, 0, 1)))

            for row in zip(*dict_of_data.values()):
                if row[0] in exsists_elements:
                    for element in row:
                        gl.add_widget(Button(text=str(element)))

            popup.dismiss()

        temp = BoxLayout(orientation='vertical')
        temp.add_widget(Spinner(text='--- Выберите тип ---',
                                values=util.get_mini_table('type_privilege'),
                                size_hint_y=None,
                                height=35,
                                id='spinner'))
        temp.add_widget(Widget())

        temp.add_widget(Button(text='Готово',
                               size_hint_y=None,
                               height=35,
                               on_press=get_data_from_db))

        popup = Popup(title='Получение льгот через их типы',
                      size_hint=(None, None),
                      size=(400, 400),
                      content=temp)
        popup.open()

    def second_query(self, gl):
        """
            Второй запрос внутренне симмистричный на получение Звонков через город и дату
            Симметричный по внешнему и дате
        :param gl:
        :return:
        """
        def get_data_from_db(instance):
            """
            Формируем результат после нажатия в Попапе Готово
            :param instance:
            :return:
            """
            city, date = None, None
            for widget in temp.children:
                if widget.id == 'spinner' and widget.text.find('---') == -1:
                    city = widget.text
                if widget.id == 'input' and widget.text:
                    date = widget.text

            if not city or not date:
                instance.background_color = (1, 0, 0, 1)
                return

            exsists_elements = util.second_query(city[:city.find(' | ')], date)

            dict_of_data = util.read_tables('Звонок')
            gl.cols = len(dict_of_data)

            for key in dict_of_data.keys():
                gl.add_widget(Button(text=key,
                                     height=50,
                                     size_hint_y=None,
                                     background_color=(0, 1, 0, 1)))

            for row in zip(*dict_of_data.values()):
                if row[0] in exsists_elements:
                    for element in row:
                        gl.add_widget(Button(text=str(element)))

            popup.dismiss()

        temp = BoxLayout(orientation='vertical')
        temp.add_widget(Spinner(text='--- Выберите город ---',
                                values=util.get_mini_table('city'),
                                size_hint_y=None,
                                height=35,
                                id='spinner'))
        temp.add_widget(TextInput(hint_text='Введите дату в формате dd.mm.yyyy',
                                  size_hint_y=None,
                                  height=35,
                                  id='input'))
        temp.add_widget(Widget())

        temp.add_widget(Button(text='Готово',
                               size_hint_y=None,
                               height=35,
                               on_press=get_data_from_db))

        popup = Popup(title='Получение звонков через город и дату',
                      size_hint=(None, None),
                      size=(400, 400),
                      content=temp)
        popup.open()

    def third_query(self, gl):
        """
            Третий запрос внутренне симитричный с датой на больший звонок
        :param gl:
        :return:
        """
        def get_data_from_db(instance):
            """
            Формируем результат после нажатия в Попапе Готово
            :param instance:
            :return:
            """
            city, date = None, None
            for widget in temp.children:
                if widget.id == 'spinner' and widget.text.find('---') == -1:
                    city = widget.text
                if widget.id == 'input' and widget.text:
                    date = widget.text

            if not city or not date:
                instance.background_color = (1, 0, 0, 1)
                return

            exsists_elements = util.third_query(city[:city.find(' | ')], date)

            dict_of_data = util.read_tables('Звонок')
            gl.cols = len(dict_of_data)

            for key in dict_of_data.keys():
                gl.add_widget(Button(text=key,
                                     height=50,
                                     size_hint_y=None,
                                     background_color=(0, 1, 0, 1)))

            for row in zip(*dict_of_data.values()):
                if row[0] in exsists_elements:
                    for element in row:
                        gl.add_widget(Button(text=str(element)))

            popup.dismiss()

        temp = BoxLayout(orientation='vertical')
        temp.add_widget(Spinner(text='--- Выберите город ---',
                                values=util.get_mini_table('city'),
                                size_hint_y=None,
                                height=35,
                                id='spinner'))
        temp.add_widget(TextInput(hint_text='Введите дату в формате dd.mm.yyyy',
                                  size_hint_y=None,
                                  height=35,
                                  id='input'))
        temp.add_widget(Widget())

        temp.add_widget(Button(text='Готово',
                               size_hint_y=None,
                               height=35,
                               on_press=get_data_from_db))

        popup = Popup(title='Получение самого длинного звонка через город и дату',
                      size_hint=(None, None),
                      size=(400, 400),
                      content=temp)
        popup.open()

    def fourth_query(self, gl):
        """
            Левое внешнее соединение, на выходе имеем АТС
        :param gl:
        :return:
        """
        def get_data_from_db(instance):
            """
            Формируем результат после нажатия в Попапе Готово
            :param instance:
            :return:
            """
            district = None
            for widget in temp.children:
                if widget.id == 'spinner' and widget.text.find('---') == -1:
                    district = widget.text
                    break
            else:
                instance.background_color = (1, 0, 0, 1)
                return

            exsists_elements = util.fourth_query(district[:district.find(' | ')])

            dict_of_data = util.read_tables('АТС')
            gl.cols = len(dict_of_data)

            for key in dict_of_data.keys():
                gl.add_widget(Button(text=key,
                                     height=50,
                                     size_hint_y=None,
                                     background_color=(0, 1, 0, 1)))

            for row in zip(*dict_of_data.values()):
                if row[0] in exsists_elements:
                    for element in row:
                        gl.add_widget(Button(text=str(element)))

            popup.dismiss()

        temp = BoxLayout(orientation='vertical')
        temp.add_widget(Spinner(text='--- Выберите район ---',
                                values=util.get_mini_table('district'),
                                size_hint_y=None,
                                height=35,
                                id='spinner'))
        temp.add_widget(Widget())

        temp.add_widget(Button(text='Готово',
                               size_hint_y=None,
                               height=35,
                               on_press=get_data_from_db))

        popup = Popup(title='Получение всех АТС по определенному району',
                      size_hint=(None, None),
                      size=(400, 400),
                      content=temp)
        popup.open()

    def fifth_query(self, gl):
        """
            Правое внешнее соединение на выходе имеем абонента
        :param gl:
        :return:
        """
        def get_data_from_db(instance):
            """
            Формируем результат после нажатия в Попапе Готово
            :param instance:
            :return:
            """
            social = None
            for widget in temp.children:
                if widget.id == 'spinner' and widget.text.find('---') == -1:
                    social = widget.text
                    break
            else:
                instance.background_color = (1, 0, 0, 1)
                return

            exsists_elements = util.fifth_query(social[:social.find(' | ')])

            dict_of_data = util.read_tables('Абонент')
            gl.cols = len(dict_of_data)

            for key in dict_of_data.keys():
                gl.add_widget(Button(text=key,
                                     height=50,
                                     size_hint_y=None,
                                     background_color=(0, 1, 0, 1)))

            for row in zip(*dict_of_data.values()):
                if row[0] in exsists_elements:
                    for element in row:
                        gl.add_widget(Button(text=str(element)))

            popup.dismiss()

        temp = BoxLayout(orientation='vertical')
        temp.add_widget(Spinner(text='--- Выберите статус ---',
                                values=util.get_mini_table('social'),
                                size_hint_y=None,
                                height=35,
                                id='spinner'))
        temp.add_widget(Widget())

        temp.add_widget(Button(text='Готово',
                               size_hint_y=None,
                               height=35,
                               on_press=get_data_from_db))

        popup = Popup(title='Получение всех абонентов по статусу',
                      size_hint=(None, None),
                      size=(400, 400),
                      content=temp)
        popup.open()

    def sixth_query(self, gl):
        """
            Левое соединение на выходе имеем звонок
        :param gl:
        :return:
        """
        def get_data_from_db(instance):
            """
            Формируем результат после нажатия в Попапе Готово
            :param instance:
            :return:
            """
            city, date = None, None
            for widget in temp.children:
                if widget.id == 'spinner' and widget.text.find('---') == -1:
                    city = widget.text
                if widget.id == 'input' and widget.text:
                    date = widget.text

            if not city or not date:
                instance.background_color = (1, 0, 0, 1)
                return

            exsists_elements = util.sixth_query(city[:city.find(' | ')], date)

            dict_of_data = util.read_tables('Звонок')
            gl.cols = len(dict_of_data)

            for key in dict_of_data.keys():
                gl.add_widget(Button(text=key,
                                     height=50,
                                     size_hint_y=None,
                                     background_color=(0, 1, 0, 1)))

            for row in zip(*dict_of_data.values()):
                if row[0] in exsists_elements:
                    for element in row:
                        gl.add_widget(Button(text=str(element)))

            popup.dismiss()

        temp = BoxLayout(orientation='vertical')
        temp.add_widget(Spinner(text='--- Выберите город ---',
                                values=util.get_mini_table('city'),
                                size_hint_y=None,
                                height=35,
                                id='spinner'))
        temp.add_widget(TextInput(hint_text='Введите дату в формате dd.mm.yyyy',
                                  size_hint_y=None,
                                  height=35,
                                  id='input'))
        temp.add_widget(Widget())

        temp.add_widget(Button(text='Готово',
                               size_hint_y=None,
                               height=35,
                               on_press=get_data_from_db))

        popup = Popup(title='Получение всех звонков до определенного\nчисла, в определенном городе',
                      size_hint=(None, None),
                      size=(400, 400),
                      content=temp)
        popup.open()

    def seventh_query(self, gl):
        """
            Запрос на данные
        :param gl:
        :return:
        """
        def get_data_from_db(instance):
            """
            Формируем результат после нажатия в Попапе Готово
            :param instance:
            :return:
            """
            price = None
            for widget in temp.children:
                if widget.id == 'input' and widget.text:
                    if widget.text.isnumeric():
                        price = widget.text
                        break
                    else:
                        widget.text, widget.hint_text_color = '', (1, 0, 0, 1)
            else:
                instance.background_color = (1, 0, 0, 1)
                return

            exsists_elements = util.seventh_query(price)

            dict_of_data = util.read_tables('Звонок')
            gl.cols = len(dict_of_data)

            for key in dict_of_data.keys():
                gl.add_widget(Button(text=key,
                                     height=50,
                                     size_hint_y=None,
                                     background_color=(0, 1, 0, 1)))

            for row in zip(*dict_of_data.values()):
                if row[0] in exsists_elements:
                    for element in row:
                        gl.add_widget(Button(text=str(element)))

            popup.dismiss()

        temp = BoxLayout(orientation='vertical')
        temp.add_widget(TextInput(hint_text='Введите цену выше которой требуется звонок',
                                  size_hint_y=None,
                                  height=35,
                                  id='input'))
        temp.add_widget(Widget())

        temp.add_widget(Button(text='Готово',
                               size_hint_y=None,
                               height=35,
                               on_press=get_data_from_db))

        popup = Popup(title='Получение всех звонков выше определенной стоимости',
                      size_hint=(None, None),
                      size=(400, 400),
                      content=temp)
        popup.open()

    def eight_query(self, gl):
        """
            Вывод с условием на группы
        :param gl:
        :return:
        """
        def get_data_from_db(instance):
            """
            Формируем результат после нажатия в Попапе Готово
            :param instance:
            :return:
            """
            ats = None
            for widget in temp.children:
                if widget.id == 'spinner' and widget.text.find('---') == -1:
                    ats = widget.text
                    break
            else:
                instance.background_color = (1, 0, 0, 1)
                return

            title_of_rows, data = util.eight_query(ats[:ats.find(' | ')])
            gl.cols = len(title_of_rows)

            for title in title_of_rows:
                gl.add_widget(Button(text=title,
                                     height=50,
                                     size_hint_y=None,
                                     background_color=(0, 1, 0, 1)))

            for row in zip(data):
                row = row[0]
                for element in row:
                    gl.add_widget(Button(text=str(element)))

            popup.dismiss()

        temp = BoxLayout(orientation='vertical')
        temp.add_widget(Spinner(text='--- Выберите АТС ---',
                                values=util.get_mini_table('ats'),
                                size_hint_y=None,
                                height=35,
                                id='spinner'))
        temp.add_widget(Widget())

        temp.add_widget(Button(text='Готово',
                               size_hint_y=None,
                               height=35,
                               on_press=get_data_from_db))

        popup = Popup(title='Получение количества зконков у определенной АТС',
                      size_hint=(None, None),
                      size=(400, 400),
                      content=temp)
        popup.open()

    def ninth_query(self, gl):
        """
            Вывод с условием на группы и данные
        :param gl:
        :return:
        """
        def get_data_from_db(instance):
            """
            Формируем результат после нажатия в Попапе Готово
            :param instance:
            :return:
            """
            ats = None
            for widget in temp.children:
                if widget.id == 'spinner' and widget.text.find('---') == -1:
                    ats = widget.text
                    break
            else:
                instance.background_color = (1, 0, 0, 1)
                return

            title_of_rows, data = util.ninth_query(ats[:ats.find(' | ')])
            gl.cols = len(title_of_rows)

            for title in title_of_rows:
                gl.add_widget(Button(text=title,
                                     height=50,
                                     size_hint_y=None,
                                     background_color=(0, 1, 0, 1)))

            for row in zip(data):
                row = row[0]
                for element in row:
                    gl.add_widget(Button(text=str(element)))

            popup.dismiss()

        temp = BoxLayout(orientation='vertical')
        temp.add_widget(Spinner(text='--- Выберите АТС ---',
                                values=util.get_mini_table('ats'),
                                size_hint_y=None,
                                height=35,
                                id='spinner'))
        temp.add_widget(Widget())

        temp.add_widget(Button(text='Готово',
                               size_hint_y=None,
                               height=35,
                               on_press=get_data_from_db))

        popup = Popup(title='Получение самого длинного звока за каждый день от определенной АТС',
                      size_hint=(None, None),
                      size=(400, 400),
                      content=temp)
        popup.open()

    def task1(self, gl):
        """
            Вывод с условием на группы и данные
        :param gl:
        :return:
        """
        def get_data_from_db(instance):
            """
            Формируем результат после нажатия в Попапе Готово
            :param instance:
            :return:
            """
            ats = None
            for widget in temp.children:
                if widget.id == 'spinner' and widget.text.find('---') == -1:
                    ats = widget.text
                    break
            else:
                instance.background_color = (1, 0, 0, 1)
                return

            title_of_rows, data = util.task1(ats[:ats.find(' | ')])
            gl.cols = len(title_of_rows)

            for title in title_of_rows:
                gl.add_widget(Button(text=title,
                                     height=50,
                                     size_hint_y=None,
                                     background_color=(0, 1, 0, 1)))

            for row in zip(data):
                row = row[0]
                for element in row:
                    gl.add_widget(Button(text=str(element)))

            popup.dismiss()

        temp = BoxLayout(orientation='vertical')
        temp.add_widget(Spinner(text='--- Выберите АТС ---',
                                values=util.get_mini_table('ats'),
                                size_hint_y=None,
                                height=35,
                                id='spinner'))
        temp.add_widget(Widget())

        temp.add_widget(Button(text='Готово',
                               size_hint_y=None,
                               height=35,
                               on_press=get_data_from_db))

        popup = Popup(title='Получение каждой категории на каждую АТС',
                      size_hint=(None, None),
                      size=(400, 400),
                      content=temp)
        popup.open()



if __name__ == '__main__':
    MyApp().run()