import datetime
import sqlite3

import checker

connect = sqlite3.connect('db.db')
cursor = connect.cursor()


name_of_table_on_rus = ('Типы привилегий', 'Город', 'Страна', 'Соц. положение', 'Районы',
                        'Льгота', 'Тариф', 'Абонент', 'АТС', 'Звонок')


rus_on_engl = {'Районы': 'district',
               'Типы привилегий': 'type_privilege',
               'Город': 'city',
               'Страна': 'country',
               'Соц. положение': 'social',
               'Льгота': 'privilege',
               'Тариф': 'tariff',
               'Абонент': 'abonent',
               'АТС': 'ats',
               'Звонок': 'call'}


fields = {'Страна': ({str(): ('Россия', 'Название страны')},),
          'Районы': ({str(): ('Кировский', 'Название района')},),
          'Тариф': ({str(): ('День', 'Тип тарифа')},
                    {str(): ('11', 'Время начала действия')},
                    {str(): ('18', 'Время окончания действия')},
                    {str(): ('37', 'Коэфициент')}),
          'Типы привилегий': ({str(): ('Инвалид', 'Тип привилегии')},),
          'Соц. положение': ({str(): ('Бизнесмен', 'Соц. положение')},),
          'Льгота': ({str(): ('Многодетная семья', 'Условие')},
                     {str(): ('Многодетка', 'Название льготы')},
                     {int(): (tuple(cursor.execute('SELECT title_of_privilege FROM type_privilege').fetchall()), 'Тип льготы')}),
          'Город': ({str(): ('Донецк', 'Название города')},
                    {int(): (tuple(cursor.execute('SELECT title_country FROM country').fetchall()), 'Страна')}),
          'Звонок': ({int(): (tuple(cursor.execute('SELECT title_of_city FROM city').fetchall()), 'Город')},
                     {str(): ('2000', 'Год основания')},
                     {str(): ('123456789', 'Номер оппонента')},
                     {str(): ('26.03.2005', 'Дата звонка')},
                     {str(): ('25', 'Длительность(мин.)')},
                     {int(): (tuple(cursor.execute('SELECT type FROM tariff').fetchall()), 'Тип тарифа')},
                     {int(): (tuple(cursor.execute('SELECT second_name || ". " || SUBSTR(first_name, 1) || ". ", SUBSTR(third_name, 1) || "." AS name FROM abonent').fetchall()), 'Абонент')},
                     {int(): (tuple(cursor.execute('SELECT title FROM ats').fetchall()), 'АТС')},
                     {int(): (tuple(cursor.execute('SELECT tariff FROM privilege').fetchall()), 'Льгота')}),
          'Абонент': ({str(): ('Владислав', 'Имя')},
                      {str(): ('Лошкарь', 'Фамилия')},
                      {str(): ('Михайлович', 'Отчество')},
                      {str(): ('123456789', 'Номер')},
                      {str(): ('Семашкино 23/4', 'Адрес')},
                      {int(): (tuple(cursor.execute('SELECT title_of_social FROM social').fetchall()), 'Соц. статус')},
                      {str(): ('Путь к картинке', 'Картинка')}),
          'АТС': ({str(): ('ООО Ацепт', 'Название')},
                  {int(): (tuple(cursor.execute('SELECT title_of_district FROM district').fetchall()), 'Район')},
                  {str(): ('Артема 45', 'Адрес')},
                  {str(): ('2005', '')},
                  {tuple(): ('', 'Государственная')},
                  {str(): ('Лицензия', 'Лицензия')})}


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
        'Абонент': ('abonent', {'ID': [], 'Имя': [], 'Фамилия': [], 'Отчество': [], 'Телефон': [], 'Адрес': [], 'Документ': [], 'Соц. положение': []}),
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
                       f'INNER JOIN country ON country.id = {name_of_table}.id_of_country '
                       f'LIMIT 50')
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


def add(name_of_table, dict_of_data):
    name_of_table = rus_on_engl.get(name_of_table)
    validation = eval('checker.' + name_of_table + '(dict_of_data)')
    if not validation[0]:
        return validation
    if dict_of_data.get(None):
        del dict_of_data[None]
    query = f'INSERT INTO {name_of_table} (' + ', '.join(dict_of_data.keys()) + ') VALUES ("' + '", "'.join(dict_of_data.values()) + '")'
    try:
        cursor.execute(query)
    except sqlite3.IntegrityError:
        return (False, 'Такая запись уже есть')
    else:
        connect.commit()
        return (True, 'Добавлено\n  успешно')


def update(name_of_table, ids, new_data):
    check = checker.check_all(new_data)
    if not check[0]:
        return check
    name_of_table = rus_on_engl.get(name_of_table)
    query = f'UPDATE {name_of_table} SET ' + ', '.join(key + ' = "' + value + '"' for key, value in new_data.items()) \
            + " WHERE id = " + ' OR id = '.join(ids.get('id'))
    try:
        cursor.execute(query)
    except sqlite3.IntegrityError:      # не укникум когда нужен уникум
        return (False, )
    except sqlite3.OperationalError:    # неверный ввод
        return (False, )
    else:
        connect.commit()
        return (True, )


def delete(name_of_table, data):
    cursor.execute(f'DELETE FROM {rus_on_engl.get(name_of_table)} WHERE id = ' + ' OR id = '.join(data))
    connect.commit()
    return None


def find(name_of_table, dict_of_data):
    result = 'SELECT id ' \
             f'FROM {rus_on_engl.get(name_of_table)} ' \
             'WHERE ' + ' AND '.join(key + ' = "' + value + '"' for key, value in dict_of_data.items())
    return read_tables(name_of_table), tuple(row[0] for row in cursor.execute(result).fetchall())


def get_fields_add(name_of_table):
    name_of_table = {'Районы': 'district',
                     'Типы привилегий': 'type_privilege',
                     'Город': 'city',
                     'Страна': 'country',
                     'Соц. положение': 'social',
                     'Льгота': 'privilege',
                     'Тариф': 'tariff',
                     'Абонент': 'abonent',
                     'АТС': 'ats',
                     'Звонок': 'call'}.get(name_of_table)
    cursor.execute(f'SELECT * FROM {name_of_table}')
    name_of_row_on_engl = (column[0] for column in cursor.description if column[0] != 'id')
    dict_of_rus_row = {'first_name': 'Имя', 'second_name': 'Фамилия', 'third_name': 'Отчество', 'phone': 'Телефон',
                       'id_of_social': 'Соц. статус', 'document': 'Документ',

                       'title': 'Название', 'id_of_district': 'Район', 'address': 'Адрес', 'year': 'Год основания',
                       'govern': 'Государственная', 'license': 'Лицензия', 'id_of_city': 'Город', 'price': 'Цена',

                       'phone_of_opponent': 'Номер оппонента', 'date_of_call': 'Дата звонка', 'duration': 'Длительность', 'id_of_tariff': 'Тариф',
                       'id_of_abonent': 'Абонент', 'id_of_ats': 'АТС', 'id_of_privileges': 'Льгота', 'title_of_city': 'Город', 'id_of_country': 'Страна',

                       'title_country': 'Страна', 'title_of_district': 'Район', 'condition': 'Условие', 'tariff': 'Тариф', 'id_of_type': 'Тип',
                       'title_of_social': 'Соц. статус', 'type': 'Тип', 'start': 'Начало', 'end': 'Конец', 'coef': 'Коэфициент', 'title_of_privilege': 'Название льготы',
                       'goverm': 'Государственная'
                       }

    name_of_row_on_rus = (dict_of_rus_row.get(column[0]) for column in cursor.description if column[0] != 'id')
    return tuple(name_of_row_on_engl), tuple(name_of_row_on_rus)


def get_mini_table(table):
    if table == 'type':
        table = 'type_privilege'
    elif table == 'privileges':
        table = 'privilege'
    return (str(row[0]) + ' | ' + row[1] for row in cursor.execute(f'SELECT * FROM {table} LIMIT 50').fetchall())


def get_fields_delete(table):
    if table == 'type':
        table = 'type_privilege'
    elif table == 'privileges':
        table = 'privilege'
    return


if __name__ == '__main__':
    # print(cursor.execute('SELECT * FROM city').fetchall())
    get_fields_add('Абонент')


def delete_on_row(name_of_table, dict_of_data):
    name_of_table = rus_on_engl.get(name_of_table)
    cursor.execute(f'SELECT id FROM {name_of_table} WHERE '+ ' AND '.join(key + ' = "' + value + '"' for key, value in dict_of_data.items()))
    list_of_pop_rows = tuple(row[0] for row in cursor.fetchall())
    query = f'DELETE FROM {name_of_table} WHERE ' + ' AND '.join(key + ' = "' + value + '"' for key, value in dict_of_data.items())
    cursor.execute(query)
    connect.commit()
    return list_of_pop_rows


def check_row(name_of_table, dict_of_old_data):
    name_of_table = rus_on_engl.get(name_of_table)
    query = 'SELECT * ' \
            f'FROM {name_of_table} WHERE ' \
            f'' + '" AND '.join((key + ' = "' + value for key, value in dict_of_old_data.items())) + '"'
    if len(cursor.execute(query).fetchall()) > 0:
        return True
    else:
        return False


def update_rows(name_of_table, dict_of_old_data, dict_of_new_data):
    name_of_table = rus_on_engl.get(name_of_table)
    check = checker.check_all(dict_of_new_data)
    if not check[0]:
        return check
    query = f'UPDATE {name_of_table} SET ' + ', '.join(key + ' = "' + value + '"' for key, value in dict_of_new_data.items()) \
            + " WHERE " + ' AND '.join(key + ' = "' + value + '"' for key, value in dict_of_old_data.items())
    try:
        cursor.execute(query)
    except:
        return (False, )
    else:
        connect.commit()
        return (True, )


#########################################################################################

######################################## ЗАПРОСЫ ########################################

#########################################################################################


def first_query(id_of_type):
    query = 'SELECT id ' \
            'FROM privilege ' \
            f'WHERE privilege.id_of_type = {id_of_type}'
    return tuple(row[0] for row in cursor.execute(query).fetchall())


def second_query(id_of_city, date):
    query = 'SELECT id ' \
            'FROM call ' \
            f'WHERE call.id_of_city = {id_of_city} ' \
            f'      AND call.date_of_call = "{date}"'
    return tuple(row[0] for row in cursor.execute(query).fetchall())


def third_query(id_of_city, date):
    query = 'SELECT id ' \
            'FROM call ' \
            f'WHERE call.id_of_city = {id_of_city} ' \
            f'      AND call.date_of_call = "{date}"' \
            'ORDER BY call.duration DESC ' \
            'LIMIT 1'
    return tuple(row[0] for row in cursor.execute(query).fetchall())


def fourth_query(id_of_district):
    query = 'SELECT ats.id ' \
            'FROM ats ' \
            f'LEFT OUTER JOIN district d on ats.id_of_district = {id_of_district}'
    return tuple(row[0] for row in cursor.execute(query).fetchall())


def fifth_query(id_of_social):
    query = 'SELECT a.id ' \
            'FROM social ' \
            f'LEFT OUTER JOIN abonent a on social.id = a.id_of_social AND social.id = {id_of_social}'
    return tuple(row[0] for row in cursor.execute(query).fetchall())


def sixth_query(id_of_city, date):
    query = 'SELECT * ' \
            'FROM call ' \
            f'LEFT JOIN city c on `call`.id_of_city = c.id AND c.id = {id_of_city} ' \
            'INNER JOIN abonent a on `call`.id_of_abonent = a.id'
    result = []
    for row in cursor.execute(query).fetchall():
        if datetime.datetime.strptime(row[4], '%d.%m.%Y') < datetime.datetime.strptime(date, '%d.%m.%Y'):
            result.append(row[0])

    return result


def seventh_query(price):
    query = 'SELECT id ' \
            'FROM call ' \
            f'WHERE call.price > {price}'
    return tuple(row[0] for row in cursor.execute(query).fetchall())


def eight_query(id_of_ats):
    query = 'SELECT c.title_of_city AS "Название города" , ' \
            '       COUNT(call.id_of_city) AS "Количество звонков" ' \
            'FROM call ' \
            'INNER JOIN city c on `call`.id_of_city = c.id ' \
            f'WHERE call.id_of_ats = {id_of_ats} ' \
            'GROUP BY c.title_of_city '
    cursor.execute(query)
    title_of_rows = tuple(title[0] for title in cursor.description)
    return title_of_rows, cursor.fetchall()


def ninth_query(id_of_ats):
    query = 'SELECT a.second_name || " " || a.first_name AS "ФИО", ' \
            '       MAX(call.duration) AS "Длительность", ' \
            '       call.date_of_call AS "Дата звонка", ' \
            '       call.phone_of_opponent AS "Номер звонившему" ' \
            'FROM call ' \
            'INNER JOIN city c on `call`.id_of_city = c.id ' \
            'INNER JOIN abonent a on `call`.id_of_abonent = a.id ' \
            f'WHERE call.id_of_ats = {id_of_ats} ' \
            'GROUP BY call.date_of_call '
    cursor.execute(query)
    title_of_rows = tuple(title[0] for title in cursor.description)
    return title_of_rows, cursor.fetchall()


def task1(id_of_ats):
    query = 'SELECT s.title_of_social AS soc,' \
            '       COUNT(s.title_of_social) AS amount ' \
            'FROM call ' \
            'INNER JOIN city c on `call`.id_of_city = c.id ' \
            'INNER JOIN abonent a on `call`.id_of_abonent = a.id ' \
            'INNER JOIN social s on a.id_of_social = s.id ' \
            f'WHERE call.id_of_ats = {id_of_ats} ' \
            'GROUP BY s.title_of_social '
    query = 'SELECT q.soc AS "Социальный статус", ' \
            '       MAX(q.amount) AS "Количество пользователей"' \
            'FROM (' + query + ') as q'
    cursor.execute(query)
    title_of_rows = tuple(title[0] for title in cursor.description)
    return title_of_rows, cursor.fetchall()
