import datetime
import re


def social(dict_of_data):
    if not dict_of_data.get('title_of_social').isalpha():
        return False, 'title_of_social', 'Вводите ТОЛЬКО буквы'
    return (True,)


def tariff(dict_of_data):
    if not dict_of_data.get('type').isalpha():
        return False, 'type', 'Вводите ТОЛЬКО буквы'
    if not re.search(r'\d{2}.\d{2}.\d{4}', dict_of_data.get('start')):
        return False, 'start', 'Введите в формате dd.mm.yyyy'
    if not re.search(r'\d{2}.\d{2}.\d{4}', dict_of_data.get('end')):
        return False, 'end', 'Введите в формате dd.mm.yyyy'
    try:
        if datetime.datetime.strptime(dict_of_data.get('start'), '%d.%m.%Y') > datetime.datetime.strptime(dict_of_data.get('end'), '%d.%m.%Y'):
            return False, 'end', 'Введенная дата меньше даты начала'
    except ValueError:
        return False, 'end', 'Введенные даты неверны'
    if not dict_of_data.get('coef').isnumeric():
        return False, 'coef', 'Не вводите буквы'
    return (True,)


def type_privilege(dict_of_data):
    if not dict_of_data.get('title_of_privilege').isalpha():
        return False, 'title_of_privilege', 'Вводите ТОЛЬКО буквы'
    return (True,)


def privilege(dict_of_data):
    return (True,)


def district(dict_of_data):
    if not dict_of_data.get('title_of_district').isalpha():
        return False, 'title_of_district', 'Вводите ТОЛЬКО буквы'
    return (True,)


def country(dict_of_data):
    if not dict_of_data.get('title_country').isalpha():
        return False, 'title_country', 'Вводите ТОЛЬКО буквы'
    return (True,)


def city(dict_of_data):
    if not dict_of_data.get('title_of_city').isalpha():
        return False, 'title_of_city', 'Вводите ТОЛЬКО буквы'
    return (True,)


def call(dict_of_data):
    if not dict_of_data.get('price').isnumeric() or len(dict_of_data.get('price')) > 4:
        return False, 'price', 'До 4ёх цифр'
    if not dict_of_data.get('phone_of_opponent').isnumeric() or len(dict_of_data.get('phone_of_opponent')) != 10:
        return False, 'phone_of_opponent', 'Должно быть 10 цифр'
    try:
        if not re.search(r'\d{2}.\d{2}.\d{4}', dict_of_data.get('date_of_call')):
            return False, 'date_of_call', 'Введите в формате dd.mm.yyyy'
        datetime.datetime.strptime(dict_of_data.get('date_of_call'), '%d.%m.%Y')
    except ValueError:
        return False, 'date_of_call', 'Введите в формате dd.mm.yyyy'
    if not dict_of_data.get('duration').isnumeric() or len(dict_of_data.get('duration')) > 3 :
        return False, 'duration', 'До 3 цифр'
    return (True,)


def ats(dict_of_data):
    if not dict_of_data.get('title').isalpha():
        return False, 'title', 'Вводите ТОЛЬКО буквы'
    if dict_of_data.get('goverm') not in ('1', '0'):
        return False, 'goverm', 'Введите 1 или 0'
    if not dict_of_data.get('year').isnumeric() or (dict_of_data.get('year').isnumeric() and (1900 > int(dict_of_data.get('year')) or int(dict_of_data.get('year')) > 2020)):
        return False, 'year', 'Должно быть число, от 1900 до 2020'
    return (True,)


def abonent(dict_of_data):
    if not dict_of_data.get('first_name').isalpha():
        return False, 'first_name', 'Вводите ТОЛЬКО буквы'
    if not dict_of_data.get('second_name').isalpha():
        return False, 'second_name', 'Вводите ТОЛЬКО буквы'
    if not dict_of_data.get('third_name').isalpha():
        return False, 'third_name', 'Вводите ТОЛЬКО буквы'
    if not dict_of_data.get('phone').isnumeric():
        return False, 'phone', 'Должно быть 10 цифр'
    return (True,)


def check_all(dict_of_data):
    if dict_of_data.get('title_of_social') and not dict_of_data.get('title_of_social').isalpha():
        return False, 'title_of_social', 'Вводите ТОЛЬКО буквы'
    if dict_of_data.get('first_name') and not dict_of_data.get('first_name').isalpha():
        return False, 'first_name', 'Вводите ТОЛЬКО буквы'
    if dict_of_data.get('second_name') and not dict_of_data.get('second_name').isalpha():
        return False, 'second_name', 'Вводите ТОЛЬКО буквы'
    if dict_of_data.get('third_name') and not dict_of_data.get('third_name').isalpha():
        return False, 'third_name', 'Вводите ТОЛЬКО буквы'
    if dict_of_data.get('phone') and not dict_of_data.get('phone').isnumeric():
        return False, 'phone', 'Должно быть 10 цифр'
    if dict_of_data.get('title') and not dict_of_data.get('title').isalpha():
        return False, 'title', 'Вводите ТОЛЬКО буквы'
    if dict_of_data.get('goverm') and dict_of_data.get('goverm') not in ('1', '0'):
        return False, 'goverm', 'Введите 1 или 0'
    if dict_of_data.get('year') and (not dict_of_data.get('year').isnumeric() or (dict_of_data.get('year').isnumeric() and (1900 > int(dict_of_data.get('year')) or int(dict_of_data.get('year')) > 2020))):
        print('sex')
        return False, 'year', 'Должно быть число, от 1900 до 2020'
    if dict_of_data.get('price') and (not dict_of_data.get('price').isnumeric() or len(dict_of_data.get('price')) > 4):
        return False, 'price', 'До 4ёх цифр'
    if dict_of_data.get('phone_of_opponent') and (not dict_of_data.get('phone_of_opponent').isnumeric() or len(dict_of_data.get('phone_of_opponent')) != 10):
        return False, 'phone_of_opponent', 'Должно быть 10 цифр'
    if dict_of_data.get('date_of_call'):
        try:
            if not re.search(r'\d{2}.\d{2}.\d{4}', dict_of_data.get('date_of_call')):
                return False, 'date_of_call', 'Введите в формате dd.mm.yyyy'
            datetime.datetime.strptime(dict_of_data.get('date_of_call'), '%d.%m.%Y')
        except ValueError:
            return False, 'date_of_call', 'Введите в формате dd.mm.yyyy'
    if dict_of_data.get('duration') and (not dict_of_data.get('duration').isnumeric() or len(dict_of_data.get('duration')) > 3):
        return False, 'duration', 'До 3 цифр'
    if dict_of_data.get('title_of_city') and not dict_of_data.get('title_of_city').isalpha():
        return False, 'title_of_city', 'Вводите ТОЛЬКО буквы'
    if dict_of_data.get('type') and not dict_of_data.get('type').isalpha():
        return False, 'type', 'Вводите ТОЛЬКО буквы'
    if (dict_of_data.get('start') and not dict_of_data.get('end')) or (dict_of_data.get('end') and not dict_of_data.get('start')):
        temp = 'end' if not dict_of_data.get('end') else 'start'
        return False, temp, 'Даты должны быть введены вместе'
    if dict_of_data.get('start') and not re.search(r'\d{2}.\d{2}.\d{4}', dict_of_data.get('start')):
        return False, 'start', 'Введите в формате dd.mm.yyyy'
    if dict_of_data.get('end') and not re.search(r'\d{2}.\d{2}.\d{4}', dict_of_data.get('end')):
        return False, 'end', 'Введите в формате dd.mm.yyyy'
    if dict_of_data.get('start') and dict_of_data.get('end'):
        try:
            if datetime.datetime.strptime(dict_of_data.get('start'), '%d.%m.%Y') > datetime.datetime.strptime(dict_of_data.get('end'), '%d.%m.%Y'):
                return False, 'end', 'Введенная дата меньше даты начала'
        except ValueError:
            return False, 'end', 'Введенные даты неверны'
    if dict_of_data.get('coef') and not dict_of_data.get('coef').isnumeric():
        return False, 'coef', 'Не вводите буквы'
    if dict_of_data.get('title_country') and not dict_of_data.get('title_country').isalpha():
        return False, 'title_country', 'Вводите ТОЛЬКО буквы'
    if dict_of_data.get('title_of_district') and not dict_of_data.get('title_of_district').isalpha():
        return False, 'title_of_district', 'Вводите ТОЛЬКО буквы'
    if dict_of_data.get('title_of_privilege') and not dict_of_data.get('title_of_privilege').isalpha():
        return False, 'title_of_privilege', 'Вводите ТОЛЬКО буквы'
    return (True,)


if __name__ == '__main__':
    print('asd123'.isnumeric())