#!/usr/bin/env python3
# coding:utf-8

import os
import sqlite3
import re


class ConsoleDict(object):
    """docstring for mydict"""
    def __init__(self):
        self.dict_name = None
        self.conn = None
        self.en_wrd = True
        self.ru_wrd = True
    
    def check_value(self, value):
        """Удаляет ненужные символы"""
        pattern = r'[^\w+]'
        return re.sub(pattern, ' ', value)[:20]

    def set_name(self, name=None):
        """Инициализирует self.dict_name при наличии базы словаря"""
        if name:
            self.dict_name = name
        else:
            self.create_base()

    def input_name(self):
        """Ввод названия словаря при его создании"""
        print('Calling ConsoleDict metod...')
        input_name = input('Введите название словаря: ')
        my_dyct_name = self.check_value(input_name)
        if my_dict_name:
            self.dict_name = my_dict_name+".sqlite3"
            # !20 символов, только буквы - дописать код
        else:
            self.dict_name = "1"+".sqlite3"

    def create_base(self):
        """Создание базы данных словаря при его изначальном отсутствии"""
        if not self.dict_name:
            self.input_name()
            self.open_base()
            cur = self.conn.cursor()
            cur.execute('CREATE TABLE if not exists words(eng_word, rus_word)')
            cur.close()
            self.conn.close()
        else:
            print("Словарь уже создан.")

    def get_name(self):
        return self.dict_name

    def open_base(self):
        self.conn = sqlite3.connect(self.dict_name)

    def add_wrd(self, eng_val, rus_val):
        """Запрос SQL на добавления слова и его перевода"""
        eng_val = self.check_value(eng_val)
        rus_val = self.check_value(rus_val)
        if eng_val and rus_val:
            cur = self.conn.cursor()
            # !30 букв на слово, только буквы, исключить др.символы - дописать код
            # удаление цифр - дописать код
            data = [eng_val, rus_val]
            sql = 'INSERT INTO words (eng_word, rus_word) VALUES (?,?)'
            cur.execute(sql, data)
            self.conn.commit()
            cur.close()

    def search_wrd(self, val):
        """Запрос SQL на поиск перевода"""
        cur = self.conn.cursor()
        # !сделать проверку val, только буквы, 30 символов - дописать код
        # удаление цифр - дописать код
        val = self.check_value(val)
        result = cur.execute('SELECT rus_word FROM words WHERE eng_word=?', (val,))
        result = list(result)
        if result:
            self.ru_wrd = result[0][0]
        else:
            self.ru_wrd = ''
        cur.close()

    def print_in_file(self):
        """Печать в файл по три пары слово-перевод в 1 строке"""
        cur = self.conn.cursor()
        result = cur.execute('SELECT * FROM words')
        result = list(result)

        all_wrd_list = []  # создание списка строк 'слово-перевод'
        for word in result:
            word = str(word[0] + '---' + word[1])
            all_wrd_list.append(word)

        file_name = self.dict_name + '.txt'
        with open(file_name, 'w') as f:
            n = 0
            for couple in all_wrd_list:
                print(couple.ljust(32), file=f, end='')
                n = n + 1  # 3 пары слов на 1 строке
                if n > 0 and n % 3 == 0:
                    print('\n', file=f, end='')

    def dell_wrd(self, val):
        """Запрос SQL на удаления слова"""
        cur = self.conn.cursor()
        cur.execute("DELETE  FROM words WHERE eng_word=?", (val,))
        self.conn.commit()
        cur.close()

    def eject_word():
        cur = self.conn.cursor()
        words = cur.execute()

    def close_base(self):
        self.conn.close()


name = None
#for file in os.listdir(os.getcwd()):
for file in os.listdir():
    if file.endswith('.sqlite3'):
        name = file

if __name__ == '__main__':
    new = ConsoleDict()
    new.set_name(name)
    if not new.get_name():
        new.create_base()
    new.open_base()

    while new.en_wrd:
        new.en_wrd = input('Введите английское слово: ')
        new.ru_wrd = input('Введите русское слово: ')
        new.add_wrd(new.en_wrd, new.ru_wrd)

    new.en_wrd = True
    while new.en_wrd:
        new.en_wrd = input('Введите слово: ')
        new.search_wrd(new.en_wrd)
        print(new.ru_wrd)

    new.close_base()
