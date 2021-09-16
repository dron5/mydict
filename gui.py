#!/usr/bin/env python3
# coding:utf-8

from consoledict import *
from tkinter import *


class GuiDict(ConsoleDict):
    """Gui for dict"""
    one_win_list = []

    def __init__(self, master):
        super(GuiDict, self).__init__()
        self.flag = False
        self.master = master
        self.set_name(name)
        self.open_base()
        self.master.title((self.dict_name).split('.')[0])
        self.in_win_state = IntVar()
        self.in_own_win_check = Checkbutton(text='в своём окне',
                                            variable=self.in_win_state)
        self.label_eng = Label(self.master, text='Англ.')
        self.label_rus = Label(self.master, text='Рус.')
        self.entry_eng = Entry(self.master, fg='green', font='arial 11')
        self.entry_rus = Entry(self.master, fg='green', font='arial 11')
        self.button_find = Button(self.master, text='Найти слово',
                                  command=self.find_wrd,
                                  fg='#800080', font='arial 13')
        self.button_add = Button(self.master,
                                 text='Добавить слово',
                                 command=self.set_wrd,
                                 fg='#800080', font='arial 13')
        self.button_del = Button(self.master, text='Удалить',
                                 command=self.delet_wrd)
        self.button_change = Button(self.master, text='В файл',
                                    command=self.save_in_file)
        self.master.geometry('450x230+200+150')
        self.button_find.grid(row=1, column=0, pady=30)
        self.button_add.grid(row=1, column=1, pady=30)
        self.label_eng.grid(row=2, column=0, padx=20)
        self.label_rus.grid(row=2, column=1, padx=70)
        self.entry_eng.grid(row=3, column=0, padx=25)
        self.entry_rus.grid(row=3, column=1, padx=45)
        self.in_own_win_check.grid(row=4, column=0)
        self.button_del.grid(row=5, column=0, pady=30)
        self.button_change.grid(row=5, column=1, pady=30)
        self.master.mainloop()

    def creat_one_word_window(self):
        """Создание отдельного окна для слова и его перевода"""
        if self.en_wrd not in GuiDict.one_win_list:  # работает с self.one_win?
            GuiDict.one_win_list.append(self.en_wrd)
            self.new_one = OneWindow(self.master, self.en_wrd, self.ru_wrd)

    def find_wrd(self):
        """Поиск перевода слова"""
        self.en_wrd = self.entry_eng.get().lower().strip()
        self.search_wrd(self.en_wrd)
        self.entry_rus.delete('0', END)
        MY_WORD = self.ru_wrd
        if not MY_WORD:
            MY_WORD = 'Нет такого слова'
        self.entry_rus.insert('0', MY_WORD)
        if self.ru_wrd:
            if self.in_win_state.get():
                self.creat_one_word_window()

    def set_wrd(self):
        """Добавление слова и его перевода в словарь"""
        self.en_wrd = self.entry_eng.get().lower().strip()
        self.ru_wrd = self.entry_rus.get().lower().strip()
        self.add_wrd(self.en_wrd, self.ru_wrd)
        self.entry_eng.delete('0', END)
        self.entry_rus.delete('0', END)

    def delet_wrd(self):
        """Удаление слова и его перевода из словаря"""
        self.en_wrd = self.entry_eng.get()
        ltext = 'Удалить слово?'
        self.confirm_dell = Confirm(self.master, ltext)
        self.flag = self.confirm_dell.ret_confirm()
        if self.flag:
            self.dell_wrd(self.en_wrd)
            self.entry_eng.delete('0', END)
            self.entry_rus.delete('0', END)
            self.flag = False

    def save_in_file(self):
        """Печать всего словаря в файл"""
        self.print_in_file()

    def input_name(self):
        self.dialog = Child(self.master)
        self.dict_name = self.dialog.ret_answer()+".sqlite3"


class OneWindow:
    """Отдельное окно для слова и его перевода"""
    def __init__(self, master, eng_wrd, rus_wrd):
        self.eng_wrd = eng_wrd
        self.rus_wrd = rus_wrd
        self.one_win = Toplevel(master)
        self.one_win.title(self.eng_wrd)
        self.label_eng = Label(self.one_win, text=self.eng_wrd, fg='blue',
                               font='arial 15')
        self.label_rus = Label(self.one_win, text=self.rus_wrd, fg='black',
                               font='arial 15')
        self.label_tab = Label(self.one_win, text='  --  ', fg='red')
        self.label_eng.pack()
        self.label_tab.pack()
        self.label_rus.pack()
        self.one_win.geometry('250x110+200+150')
        self.one_win.protocol("WM_DELETE_WINDOW", self.on_closing)

    def rem_wrd(self):
        """Удаление слова из переменной класса GuiDict"""
        GuiDict.one_win_list.remove(self.eng_wrd)

    def on_closing(self):
        self.rem_wrd()
        self.one_win.destroy()


class Child:
    """Создаёт словарь при его  отсутствии"""
    def __init__(self, master):
        self.slave = Toplevel(master)
        self.answer = ''
        self.slave.title('child')
        self.slave.geometry('200x150+100+50')
        self.text = Entry(self.slave)
        self.text.pack(side=TOP)
        self.button = Button(self.slave, text='Создать словарь',
                             command=self.creat_answer)
        self.button.pack(side=BOTTOM)

    def ret_answer(self):
        self.slave.grab_set()
        self.slave.focus_set()
        self.slave.wait_window()
        return self.answer

    def creat_answer(self):
        self.answer = self.text.get()
        self.slave.destroy()


class Confirm:
    """Диалоговое окно при удалении слова"""
    def __init__(self, master, ltext):
        self.conf_flag = ''
        self.confirm = Toplevel(master)
        self.confirm.title(ltext)
        self.confirm.geometry('250x150')
        self.label_ltext = Label(self.confirm, text=ltext)
        self.button_yes = Button(self.confirm, text='Да',
                                 command=self.answer_yes)
        self.button_no = Button(self.confirm, text='Нет',
                                command=self.answer_no)

        self.label_ltext.grid(row=1, column=1, padx=5, pady=20)
        self.button_yes.grid(row=2, column=1)
        self.button_no.grid(row=2, column=2)

    def ret_confirm(self):
        self.confirm.grab_set()
        self.confirm.focus_set()
        self.confirm.wait_window()
        return self.conf_flag

    def answer_yes(self):
        self.conf_flag = 'yes'
        self.confirm.destroy()

    def answer_no(self):
        self.confirm.destroy()


root = Tk()
GuiDict(root)
