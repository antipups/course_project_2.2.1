import re
import sqlite3
import random


with open('rocid.xml', 'r', encoding='utf-8') as f:
    text = f.read()
text = re.findall(r'<name>[^\n]*', text)
text = tuple(map(lambda word: word[word.find('>') + 1:word.rfind('<')], text))
text = 'INSERT INTO city (title_of_city, id_of_country) VALUES ("' + '), ("'.join(word + '", ' + str(random.randint(1, 12)) + '' for word in text) + ')'

print(text)
connect = sqlite3.connect('db.db')
cursor = connect.cursor()

cursor.execute(text)