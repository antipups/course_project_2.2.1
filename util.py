import sqlite3


connect = sqlite3.connect('db.db')
cursor = connect.cursor()


def has_user(login, password):
    """
        Авторизация
    :param login:
    :param password:
    :return:
    """
    cursor.execute('SELECT * '
                   f'FROM users '
                   f'WHERE login="{login}" AND password="{password}"')
    return bool(cursor.fetchall())


def reg_user(login, password):
    """
        Регистарцию пользователя
    :param login:
    :param password:
    :return:
    """
    cursor.execute('SELECT * '
                   f'FROM users '
                   f'WHERE login="{login}"')
    if cursor.fetchall() or not login or not password:
        return False
    else:
        cursor.execute('INSERT INTO users (login, password)'
                       f'VALUES ("{login}", "{password}")')
        connect.commit()
        return True


def read_tables(name_of_table_rus):
    data_of_table = {
        'Районы': ('district', {'ID': [], 'Название страны': []}),
        'Типы привилегий': ('type_privilege', {'ID': [], 'Название типа льготы': []}),
        'Город': ('city', {'ID': [], 'Название города': [], 'Страна': []}),
        'Страна': ('country', {'ID': [], 'Название страны': []}),
        'Соц. положение': ('social', {'ID': [], 'Название соц. положения': []}),
        'Льгота': ('privilege', {'ID': [], 'Условие по оплате': [], 'Тариф льготы': [], 'Тип льготы': []}),
        'Тариф': ('tariff', {'ID': [], 'Тип тарифа': [], 'Дата начала': [], 'Дата конца': [], 'Коэфициент': []}),
        'Абонент': ('abonent', {'ID': [], 'Фамилия': [], 'Имя': [], 'Отчество': [], 'Телефон': [], 'Адрес': [], 'Документ на льготу': [], 'Социальное положение': []}),
        'АТС': ('ats', {'ID': [], 'Название': [], 'Район': [], 'Адрес': [], 'Год открытия': [], 'Государственная (бул)': [], 'Лицензиая на оказ услуг': []}),
        'Звонок': ('call', {'ID': [], 'Цена': [], 'Номер телефона': [], 'Дата звонка': [], 'Длительность': [], 'Тариф': [], 'Абонент': [], 'АТС': [], 'Льгота': [], 'Город': []}),
    }.get(name_of_table_rus)

    name_of_table, dict_of_data = data_of_table

    if name_of_table_rus in ('Районы', 'Типы привилегий', 'Соц. положение', 'Тариф', 'Страна'):
        cursor.execute(f'SELECT * FROM {name_of_table}')
        for row in cursor.fetchall():
            for index, key in enumerate(dict_of_data.keys()):
                dict_of_data[key].append(row[index])

    elif name_of_table_rus == 'Город':
        cursor.execute(f'SELECT * '
                       f'FROM {name_of_table} '
                       f'INNER JOIN country ON country.id = {name_of_table}.id_of_country')
        for row in cursor.fetchall():
            row = row[:2] + row[4:]
            for index, key in enumerate(dict_of_data.keys()):
                dict_of_data[key].append(row[index])

    elif name_of_table_rus == 'Льгота':
        cursor.execute(f'SELECT * '
                       f'FROM {name_of_table} '
                       f'INNER JOIN type_privilege ON type_privilege.id = {name_of_table}.id_of_type')
        for row in cursor.fetchall():
            row = row[:3] + row[5:]
            for index, key in enumerate(dict_of_data.keys()):
                dict_of_data[key].append(row[index])

    elif name_of_table_rus == '':
        cursor.execute(f'SELECT * '
                       f'FROM {name_of_table} '
                       f'INNER JOIN type_privilege ON type_privilege.id = {name_of_table}.id_of_type')
        for row in cursor.fetchall():
            row = row[:3] + row[5:]
            for index, key in enumerate(dict_of_data.keys()):
                dict_of_data[key].append(row[index])

    return dict_of_data
    # print(cursor.fetchall())