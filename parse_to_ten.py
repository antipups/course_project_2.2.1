# import re
# import sqlite3
# import random
#
#
# with open('rocid.xml', 'r', encoding='utf-8') as f:
#     text = f.read()
# text = re.findall(r'<name>[^\n]*', text)
# text = tuple(set(tuple(map(lambda word: word[word.find('>') + 1:word.rfind('<')], text))))
# text = list(text)
# connect = sqlite3.connect('db.db')
# cursor = connect.cursor()
# for i in tuple(x[0] for x in cursor.execute('SELECT title_of_city FROM city').fetchall()):
#     text.remove(i)
# text = 'INSERT INTO city (title_of_city, id_of_country) VALUES ("' + '), ("'.join(word + '", ' + str(random.randint(1, 12)) + '' for word in text) + ')'
#
# print(text)
#
# cursor.execute(text)
# connect.commit()
# connect.close()


# 'DELETE FROM city WHERE id > 0 '