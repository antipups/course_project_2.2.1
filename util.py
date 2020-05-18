import sqlite3


connect = sqlite3.connect('db.db')
cursor = connect.cursor()


name_of_table_on_rus = ('Типы привилегий', 'Город', 'Страна', 'Соц. положение', 'Районы',
                        'Льгота', 'Тариф', 'Абонент', 'АТС', 'Звонок')
fields = {'Страна': ({str(): 'Россия'},),
          'Районы': ({str(): 'Кировский'},),
          'Тариф': ({str(): 'День'},
                    {str(): '11'},
                    {str(): '18'},
                    {str(): '37'}),
          'Типы привилегий': ({str(): 'Инвалид'},),
          'Соц. положение': ({str(): 'Бизнесмен'},),
          'Льгота': ({str(): 'Многодетная семья'},
                     {str(): 'Название льготы'},
                     {int(): tuple(cursor.execute('SELECT title_of_privilege FROM type_privilege').fetchall())}),
          'Город': ({str(): 'Донецк'},
                    {int(): tuple(cursor.execute('SELECT title_country FROM country').fetchall())}),
          'Звонок': ({int(): tuple(cursor.execute('SELECT title_of_city FROM city').fetchall())},
                     {str(): '2000'},
                     {str(): '123456789'},
                     {str(): '26.03.2005'},
                     {str(): '25'},
                     {int(): tuple(cursor.execute('SELECT type FROM tariff').fetchall())},
                     {int(): tuple(cursor.execute('SELECT second_name || ". " || SUBSTR(first_name, 1) || ". ", SUBSTR(third_name, 1) || "." AS name FROM abonent').fetchall())},
                     {int(): tuple(cursor.execute('SELECT title FROM ats').fetchall())},
                     {int(): tuple(cursor.execute('SELECT tariff FROM privilege').fetchall())}),
          'Абонент': ({str(): 'Владислав'},
                      {str(): 'Лошкарь'},
                      {str(): 'Михайлович'},
                      {str(): '123456789'},
                      {str(): 'Семашкино 23/4'},
                      {int(): tuple(cursor.execute('SELECT title_of_social FROM social').fetchall())},
                      {str(): 'Путь к картинке'}),
          'АТС': ({str(): 'ООО Ацепт'},
                  {int(): tuple(cursor.execute('SELECT title_of_district FROM district').fetchall())},
                  {str(): 'Артема 45'},
                  {str(): '2005'},
                  {tuple(): ''},
                  {str(): 'Лицензия'})}


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
    """
        Вывод таблиц на окно
    :param name_of_table_rus:
    :return:
    """
    data_of_table = {
        'Районы': ('district', {'ID': [], 'Название страны': []}),
        'Типы привилегий': ('type_privilege', {'ID': [], 'Название типа льготы': []}),
        'Город': ('city', {'ID': [], 'Название города': [], 'Страна': []}),
        'Страна': ('country', {'ID': [], 'Название страны': []}),
        'Соц. положение': ('social', {'ID': [], 'Название соц. положения': []}),
        'Льгота': ('privilege', {'ID': [], 'Условие по оплате': [], 'Тариф льготы': [], 'Тип льготы': []}),
        'Тариф': ('tariff', {'ID': [], 'Тип тарифа': [], 'Дата начала': [], 'Дата конца': [], 'Коэфициент': []}),
        'Абонент': ('abonent', {'ID': [], 'Фамилия': [], 'Имя': [], 'Отчество': [], 'Телефон': [], 'Адрес': [], 'Документ': [], 'Соц. положение': []}),
        'АТС': ('ats', {'ID': [], 'Название': [], 'Район': [], 'Адрес': [], 'Год открытия': [], 'Государственная': [], 'Лицензия': []}),
        'Звонок': ('call', {'ID': [], 'Город': [], 'Цена': [], 'Номер телефона': [], 'Дата звонка': [], 'Длительность': [], 'Тариф': [], 'Абонент': [], 'АТС': [], 'Льгота': []}),
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

    elif name_of_table_rus == 'АТС':
        cursor.execute(f'SELECT * '
                       f'FROM {name_of_table} '
                       f'INNER JOIN district ON district.id = {name_of_table}.id_of_district')
        for row in cursor.fetchall():
            row = list(row)
            row[-4] = 'Да' if row[-4] == 1 else 'Нет'
            del row[2]
            row.insert(2, row.pop(-1))
            for index, key in enumerate(dict_of_data.keys()):
                dict_of_data[key].append(row[index])

    elif name_of_table_rus == 'Абонент':
        cursor.execute(f'SELECT * '
                       f'FROM {name_of_table} '
                       f'INNER JOIN social ON social.id = {name_of_table}.id_of_social')
        for row in cursor.fetchall():
            row = list(row)
            del row[6], row[-2]
            row.insert(7, row.pop(-1))
            for index, key in enumerate(dict_of_data.keys()):
                dict_of_data[key].append(row[index])

    elif name_of_table_rus == 'Звонок':
        cursor.execute(f'SELECT * '
                       f'FROM {name_of_table} '
                       f'INNER JOIN city ON city.id = {name_of_table}.id_of_city '
                       f'INNER JOIN tariff ON tariff.id = {name_of_table}.id_of_tariff '
                       f'INNER JOIN abonent ON abonent.id = {name_of_table}.id_of_abonent '
                       f'INNER JOIN ats ON ats.id = {name_of_table}.id_of_ats '
                       f'INNER JOIN privilege ON privilege.id = {name_of_table}.id_of_privileges '
                       )
        for row in cursor.fetchall():
            row = list(row)
            row[1], row[6], row[7], row[8], row[9] = row[11], row[14], row[20] + ' ' + row[19][0] + '. ' + row[21][0] + '.', row[27], row[34],
            del row[10:]
            for index, key in enumerate(dict_of_data.keys()):
                dict_of_data[key].append(row[index])

    return dict_of_data


def add(name_of_table, **data):
    print(name_of_table, data)
    return None


def update(name_of_table, **data):
    print(name_of_table, data)
    return None


def delete(name_of_table, **data):
    print(name_of_table, data)
    return None


def find(name_of_table, **data):
    print(name_of_table, data)
    return None


if __name__ == '__main__':
    print(cursor.execute('SELECT * FROM city').fetchall())