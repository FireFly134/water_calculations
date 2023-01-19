"""
https://yandex.ru/search/?text=tkinter+%D0%BA%D0%B0%D0%BA+%D0%BE%D1%82%D0%BA%D1%80%D1%8B%D0%B2%D0%B0%D1%82%D1%8C+%D0%B4%D1%80%D1%83%D0%B3%D0%B8%D0%B5+%D0%BE%D0%BA%D0%BD%D0%B0+%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D1%8B&lr=114900&clid=2270455&win=410
https://pythonru.com/uroki/vsplyvajushhie-okna-tkinter-11

скролл гдя года
https://translated.turbopages.org/proxy_u/en-ru.ru.48baf219-63a34409-f8d77d32-74722d776562/https/stackoverflow.com/questions/71677889/create-a-scrollbar-to-a-full-window-tkinter-in-python
"""
# -*- coding: utf-8 -*-
import os
import sys
from calendar import monthrange
# from time import sleep
from random import uniform, sample
from threading import Thread

from tkinter import *
from tkinter.ttk import Progressbar, Combobox
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from PIL import ImageTk, Image

rand_opt = False #вкл или выкл рандома
year = 2022
num_people = 1000
# q_people = 100

list_values = {"day": [],
                "cb_day": [],
                "week": [],
                "cb_week": [],
                "year":  [],
                "cb_year":  [],
               }

### Основное приложение TKinter ###
class main_app(Tk):
    def __init__(self):
        super().__init__()
        self.title("Программа для расчета потребления воды")
        self.resizable(width=False, height=False) # Запрещаем увеличивать размеры окна
        if getattr(sys, 'frozen', False): # Проверяем создаёт ли программа временные файлы
            self.application_path = sys._MEIPASS # сохраняем путь до временных файлов
        elif __file__:
            self.application_path = os.path.dirname(__file__) # Если временных файлов нет, а это только когда программа не скомпилированна, берем нужные файлы рядом с папкой
        iconFile = 'ivea_icon.ico' # название файла иконки для приложения
        self.iconbitmap(default=os.path.join(self.application_path, iconFile)) # Открываем иконку для отображения в программе
        self.check() # Проверяем на наличие около программы документов, в противном случае достаем из корня программы файлы по дефолту
        self.main() # Открываем основное окно и рисуем интерфейс.

    def main(self):
        w = int(640/1.5)
        h = int(480/1.5)
        self.test_entry = StringVar(name="num_people")
        self.test2_entry = StringVar(name="center_value_day")
        self.test3_entry = StringVar(name="q_people")
        self.test_entry.set(str(num_people))
        self.test2_entry.set("")
        self.test3_entry.set("100")
        self.test_entry.trace_id = self.test_entry.trace('w', self.test)
        self.test2_entry.trace_id = self.test2_entry.trace('w', self.test)
        self.test3_entry.trace_id = self.test3_entry.trace('w', self.test)
        self.progressbar = Progressbar(self, orient=HORIZONTAL, length=400, mode='determinate')
        self.label = Label(self, text="")
        self.year = Entry(self)  # Введите год цифрами
        self.num_people = Entry(self, textvariable=self.test_entry)  # Введите количество человек цифрами, к примеру 2000
        self.num_people.config(validate="key", validatecommand=(self.num_people.register(self.check_keys), '%P'))
        # self.q_people = Entry(self)  # Введите удельную норму водоотведения на одного жителя (л/сут), цифрами, к примеру 150
        self.center_value_day = Entry(self, textvariable=self.test2_entry)
        self.button = Button(self, text="Произвести расчет", command=self.calculations)
        self.year.insert(0, str(year))
        # self.year_lab = Label(self, text="Введите год:")#, к примеру 2022
        # self.num_people.insert(0, str(num_people))
        self.num_people_lab = Label(self, text="Введите количество человек:")# цифрами, к примеру 2000"
        self.q_people = Combobox(self, values=["80", "100", "120", "150", "200", "300", "350"], textvariable=self.test3_entry)
        # self.q_people.current(1)
        # self.q_people.insert(0, str(q_people))
        self.q_people_lab = Label(self, text="Введите удельную норму водоотведения на одного жителя (л/сут):")#, цифрами, к примеру 150"
        # self.center_value_day.insert(0, str(q_people))
        self.center_value_day_lab = Label(self, text="Введите среднесуточный расход (м\u00B3/сут):")
        # self.year.grid(column=1, row=0, sticky="w")
        # self.year_lab.grid(column=0, row=0, sticky="w")
        # self.num_people.focus_set()
        # self.q_people.focus_set()
        # self.center_value_day.focus_set()
        # self.year.focus_set()
        if not os.path.exists(f"{os.getcwd()}/excel_chart_day.jpeg"):
            img = Image.open(os.path.join(self.application_path, 'excel_chart_day.jpeg'))
        else:
            img = Image.open(f"{os.getcwd()}\excel_chart_day.jpeg")
        resize_image =  img.resize((w, h))
        img  = ImageTk.PhotoImage(resize_image)
        if not os.path.exists(f"{os.getcwd()}/excel_chart_week.jpeg"):
            img2 = Image.open(os.path.join(self.application_path, 'excel_chart_week.jpeg'))
        else:
            img2 = Image.open(f"{os.getcwd()}\excel_chart_week.jpeg")
        resize_image = img2.resize((w, h))
        img2 = ImageTk.PhotoImage(resize_image)
        if not os.path.exists(f"{os.getcwd()}/excel_chart_year.jpeg"):
            img3 = Image.open(os.path.join(self.application_path, 'excel_chart_year.jpeg'))
        else:
            img3 = Image.open(f"{os.getcwd()}\excel_chart_year.jpeg")
        resize_image = img3.resize((w, h))
        img3 = ImageTk.PhotoImage(resize_image)
        l = Label(self)
        l2 = Label(self)
        l3 = Label(self)
        l.image = img
        l2.image = img2
        l3.image = img3
        l["image"] = l.image
        l2["image"] = l2.image
        l3["image"] = l3.image
        self.btn = Button(self, text="Открыть папку с файлами",
                          command=self.open_window)
        self.btn2 = Button(self, text="Открыть суточный редактор", image=img,
                          command=self.open_window_day)
        self.btn3 = Button(self, text="Открыть недельный редактор", image=img2,
                           command=self.open_window_week)
        self.btn4 = Button(self, text="Открыть годовой редактор", image=img3,
                           command=self.open_window_year)
        self.btn5 = Button(self, text="рассчитать", command=self.test)

        self.num_people.grid(column=1, row=1, sticky="w")
        self.num_people_lab.grid(column=0, row=1, sticky="w")
        self.q_people.grid(column=1, row=2, sticky="w")
        self.q_people_lab.grid(column=0, row=2, sticky="w")
        # self.btn5.grid(column=2, row=2, sticky="w")
        self.center_value_day.grid(column=1, row=3, sticky="w")
        self.center_value_day_lab.grid(column=0, row=3, sticky="w")

        self.btn2.grid(column=0, row=4)
        self.btn3.grid(column=1, row=4)
        self.btn4.grid(column=2, row=4)

        self.progressbar.grid(columnspan=3, row=5)
        self.label.grid(columnspan=3, row=6)
        self.button.grid(columnspan=3, row=7)
        self.btn.grid(columnspan=3, row=8)
        # self.button2 = Button(self, text="Произвести расчет(из эксель)", command=self.calculations2)
        # self.button2.grid(columnspan=3, row=8)

    def test(self,q,w,e):#qwe переменные необходимые для работы StringVar()
        # pass
        self.test_entry.trace_vdelete("w", self.test_entry.trace_id)
        self.test2_entry.trace_vdelete("w", self.test2_entry.trace_id)
        # print(self.test_entry.trace_vinfo()[0][1])
        # print(self.test_entry.trace_vinfo())
        # print(self.test2_entry.trace_vinfo())

        # print(q)
        # print(w)
        # print(e)
        print(self.num_people.get())
        try:
            print(self.q_people.get())
        except Exception:
            pass
        # self.center_value_day.insert(0, str(int(self.center_value_day.get())+1))
        self.test_entry.set(str(int(self.num_people.get())+1))
        if self.center_value_day.get() == '':
            self.test2_entry.set("1")
        else:
            self.test2_entry.set(str(int(self.center_value_day.get())+1))
        self.test_entry.trace_id = self.test_entry.trace("w", self.test)
        self.test2_entry.trace_id = self.test2_entry.trace("w", self.test)

    def calculations(self):
        self.label['text'] = "                       "
        self.update_idletasks()
        df = main(year=int(self.year.get()), num_people=int(self.num_people.get()), q_people=int(self.q_people.get()))
        df2 = chart_year(df)
        faind_max_min_in_day(df2)
        faind_max_min_in_hour(df2)

    # def calculations2(self):
    #     self.label['text'] = "                       "
    #     self.update_idletasks()
    #     df = pd.read_excel(f"{os.getcwd()}/expense_schedule.xlsx")
    #     self.label['text'] = "40%"
    #     self.update_idletasks()
    #     df2 = chart_year(df)
    #     print(df2)
    #     self.label['text'] = "70%"
    #     self.update_idletasks()
    #     faind_max_min_in_hour(df2)
    #     self.label['text'] = "90%"
    #     self.update_idletasks()
    #     faind_max_min_in_day(df2)
    #     self.label['text'] = "Готово"
    #     self.update_idletasks()

    def open_window(self):
        os.system(f"explorer {os.getcwd()}")

    def open_window_day(self):
        self.check()
        self.save_glob()
        num = 24
        label_x = 'Час'
        label_y = 'коэфф.'
        description = f"График за день"
        name = 'day'
        about2 = win_setting(self, num, label_x, label_y, description, name)
        about2.grab_set()

    def open_window_week(self):
        self.check()
        self.save_glob()
        num = 7
        label_x = 'номер недели'
        label_y = 'коэфф.'
        description = f"График за неделю"
        name = 'week'

        about2 = win_setting(self, num, label_x, label_y, description, name)
        about2.grab_set()

    def open_window_year(self):
        self.check()
        self.save_glob()
        about2 = win_setting_for_year(self)
        about2.grab_set()

# тут мы просто сохраняем глобальные переменные...
    def save_glob(self):
        global year, num_people, q_people
        year = int(self.year.get())
        num_people = int(self.num_people.get())
        q_people = int(self.q_people.get())

# Проверка на наличие необходимых файлов и их открытие.
    def check(self):
        global list_values
        if os.path.exists(f"{os.getcwd()}/day.xlsx"):
            df_day = pd.read_excel(f"{os.getcwd()}/day.xlsx")
        else:
            df_day = pd.read_excel(os.path.join(self.application_path, "day.xlsx"))
        list_values["day"] = df_day['k'].to_list()
        list_values["cb_day"] = df_day['chekBox'].to_list()

        if os.path.exists(f"{os.getcwd()}/week.xlsx"):
            df_week = pd.read_excel(f"{os.getcwd()}/week.xlsx")
        else:
            df_week = pd.read_excel(os.path.join(self.application_path, "week.xlsx"))
        list_values["week"] = df_week['k'].to_list()
        list_values["cb_week"] = df_week['chekBox'].to_list()

        if os.path.exists(f"{os.getcwd()}/year.xlsx"):
            df_year = pd.read_excel(f"{os.getcwd()}/year.xlsx")
        else:
            df_year = pd.read_excel(os.path.join(self.application_path, "year.xlsx"))
        list_values["year"] = df_year['k'].to_list()
        list_values["cb_year"] = df_year['chekBox'].to_list()

# Валидация ввода символов в ячейки ввода.
    def check_keys(self, text):
        list_punctuation_marks="!@#$%^&*()_-+=[{}]\|/,?><:;'\"`~ "
        # Не событие вставки или ни один символ в тексте не является буквой
        return not any(char.isalpha() for char in text) and not any(char in list_punctuation_marks for char in text)

class win_setting(Toplevel):
    global list_values
    def __init__(self, parent, num, label_x, label_y, description, name, num_month=0):
        super().__init__(parent)
        self.scale_list = []
        self.cb = {"box": [],
                   "val": [],
                   "StringVar": [],
                   "entry": []}
        self.v = []
        self.num = num # кол-во элементов
        self.num_day = 0
        self.num_month = num_month
        self.label_x = label_x
        self.label_y = label_y
        self.description = description
        self.name = name
        self.title(f"Chart_{name}")
        self.resizable(width=False, height=False)

        win_setting.protocol(self, "WM_DELETE_WINDOW", self.close_window)
        self.main_class()

    def main_class(self):
        l = []
        if self.name == "year":
            for m in range(1, self.num_month):
                num = int(monthrange(year, m)[1])
                self.num_day += num
            for j in range(len(list_values["year"])):
                self.cb["box"].append(IntVar())
                self.cb["box"][j].set(list_values["cb_year"][j])

                self.cb["val"].append(list_values["cb_year"][j])  # Вопрос в том, можно ли обойтись без этого?

                self.v.append(DoubleVar())
                self.v[j].set(list_values["year"][j])
            for i in range(self.num_day, self.num_day + self.num):
                l.append(Label(self))
                l[i - self.num_day].config(text=str(i - self.num_day + 1))
                Checkbutton(self, variable=self.cb["box"][i], command=self.magic_checkbox).grid(column=i - self.num_day, row=1,sticky="e")
                self.scale_list.append(Scale(self, variable=self.v[i], from_=2.0, to=0.0, orient=VERTICAL, resolution=0.01, bd=0, length=300))#, command=self.magic
                self.scale_list[i - self.num_day].grid(column=i - self.num_day, row=2)
                l[i - self.num_day].grid(column=i - self.num_day, row=3)
                if self.cb["val"][i] == 1:
                    self.scale_list[i - self.num_day].configure(state='disabled')
        else:
            for i in range(self.num):
                # Создаём чекбокс
                self.cb["box"].append(IntVar())
                self.cb["box"][i].set(list_values[f"cb_{self.name}"][i])

                # Создаём ползунок и помещаем туда значение
                self.v.append(DoubleVar(name=str(i)))
                self.v[i].set(list_values[self.name][i])

                # Создаём переменную для хранения значений с ячейки для ввода и реагирующую на изменения
                self.cb["StringVar"].append(StringVar(name=str(i)))#(name=f"index={i}"))
                # self.cb["StringVar"][i].set(round(list_values[self.name][i], 2))
                # self.cb["StringVar"][i].trace_id = self.cb["StringVar"][i].trace('w', self.magic_entry)


                self.cb["val"].append(list_values[f"cb_{self.name}"][i]) # Вопрос в том, можно ли обойтись без этого?

                # Создаём ячейку для ввода
                self.cb["entry"].append(Entry(self, width=5, textvariable=self.cb["StringVar"][i]))
                self.cb["entry"][i].config(validate="key", validatecommand=(self.cb["entry"][i].register(self.check_keys), '%P'))

                l.append(Label(self))

                if self.name == "day":
                    from_scale = 4.0
                    l[i].config(text=str(i + 1)+"ч.")
                else:
                    from_scale = 2.0
                    l[i].config(text=str(i + 1))

                Checkbutton(self, variable=self.cb["box"][i], command=self.magic_checkbox).grid(column=i, row=1, sticky="e")

                self.scale_list.append(Scale(self, variable=self.v[i], from_=from_scale, to=0.0, orient=VERTICAL, resolution=0.01, bd=0, length=300))#, command=self.magic))
                l[i].grid(column=i, row=2)
                self.scale_list[i].grid(column=i, row=3)
                self.cb["entry"][i].grid(column=i, row=4)
                if self.cb["val"][i] == 1:
                    self.scale_list[i - self.num_day].configure(state='disabled')
                    self.cb["entry"][i - self.num_day].configure(state='disabled')

            # Когда со всеми присваиваю функцию возникает ошибка, а так нет.
            for i in range(self.num):
                # self.cb["StringVar"][i].set(round(list_values[self.name][i], 2))
                self.cb["StringVar"][i].trace_id = self.cb["StringVar"][i].trace('w', self.magic_entry)

        self.button = Button(self, text="Сохранить", command=self.select)
        self.button2 = Button(self, text="Закрыть", command=self.close_window)
        self.button3 = Button(self, text="Сбросить всё на единицы", command=self.default)
        # self.button4 = Button(self, text="Отменить всё", command=self.main_class)

        self.button.grid(columnspan=55, row=5)
        self.button2.grid(columnspan=55, row=6)
        self.button3.grid(columnspan=55, row=0, sticky="w")
        # self.button4.grid(columnspan=10, column=2, row=0)
        # self.lable_test = Label(self)
        # self.lable_test.grid(columnspan=55, row=6)
    def select(self):
        if self.name == "day":
            name_column = "hour"
        elif self.name == "week":
            name_column = "week"
        else:
            name_column = "day"
        rez = {name_column: [],
               "k": [],
               "chekBox": []
               }
        for i in range(len(list_values[self.name])): #Нужно ли эта перезапись?
            rez[name_column].append(i+1)
            rez["k"].append(list_values[self.name][i])
            rez["chekBox"].append(self.cb["val"][i])
        df = pd.DataFrame(rez)
        df.to_excel(f"{os.getcwd()}/{self.name}.xlsx", index=None)

        self.list_x = rez[name_column]
        self.list_y = rez["k"]
        self.file_name = f'excel_chart_{self.name}.jpeg'
        self.chart()

# отвечает за функционал черкбоксов, отслеживает было ли сделано действие и какое.
    def magic_checkbox(self):
        # Перебираем все значения
        for i in range(self.num_day, self.num_day + self.num):
            # Если значение отличается от того какое у нас было записано, то выполняем действие.
            if self.cb["box"][i].get() != self.cb["val"][i]:
                # Обязательно следим чтобы осталось не меньше 2х не активированых чекбоксов. Иначе просто не даем нажимать на них.
                if self.cb["val"].count(0) == 2:
                    if self.cb["box"][i].get() == 1:
                        self.cb["box"][i].set(0)
                # Ну и на реакцию действия деактивируем или активируем возможнось изменения значений. И все фиксируем соответственно.
                if self.cb["box"][i].get() == 0:
                    self.cb["val"][i] = 0
                    self.scale_list[i - self.num_day].configure(state='active')
                    self.cb["entry"][i - self.num_day].configure(state='normal')
                else:
                    self.cb["val"][i] = 1
                    self.scale_list[i - self.num_day].configure(state='disabled')
                    self.cb["entry"][i - self.num_day].configure(state='disabled')
    # def magic_old(self, value):
    #     # print(value)
    #     for i in range(self.num_day, self.num_day + self.num):
    #         if self.v[i].get() != list_values[self.name][i]:
    #             if self.name != "year":
    #                 if self.cb["val"].count(1) == 0:
    #                     z = (list_values[self.name][i]-self.v[i].get())/(self.num-1)
    #                 else:
    #                     z = (list_values[self.name][i]-self.v[i].get())/(self.cb["val"].count(0)-1)
    #                 for j in range(len(list_values[self.name])):
    #                     list_values_vrem = []
    #                     if j != i and self.cb["val"][j] != 1:
    #                         list_values_vrem.append(self.v[j].get())
    #                     if j != i and self.cb["val"][j] != 1:
    #                         if list_values_vrem.count(0) > 0 or list_values_vrem.count(2) > 0:
    #                             # self.scale_list[i].configure(state='disabled')
    #                             if (list_values_vrem.count(0) > 0 and z > 0) or (list_values_vrem.count(2) > 0 and z < 0):
    #                                 self.v[j].set(self.v[j].get() + z)
    #                             print(list_values[self.name])
    #                             print(i)
    #                             self.v[i].set(list_values[self.name][i])
    #                         else:
    #                             self.v[j].set(self.v[j].get() + z)
    #                     list_values[self.name][j] = self.v[j].get()
    #             else:
    #                 z = (list_values[self.name][i] - self.v[i].get()) / 365
    #                 for j in range(len(list_values[self.name])):
    #                     if j != i:
    #                         self.v[j].set(self.v[j].get() + z)
    #                     list_values[self.name][j] = self.v[j].get()
    #
    #             break

    def magic_entry(self, idx, q='', w=''):
        const_val = 0
        no_const_val = 0
        no_const_list_index = []
        idx = int(idx)
        if str(self.cb["StringVar"][idx].get()) != "" and str(self.cb["StringVar"][idx].get()) != ".":
            value = round(float(self.cb["StringVar"][idx].get()), 2)
            # Сначала рассчитываем значение которые имеются, фиксированные и не фиксированные...
            for i in range(self.num_day, self.num_day + self.num):
                v_get = round(float(self.cb["StringVar"][i].get()), 2)
                if self.cb["val"][i] == 1:
                    const_val += v_get
                else:
                    if v_get != value:
                        no_const_val += v_get
                        no_const_list_index.append(i)

            ### Расчет минимального и максимального значения ###
            max = self.num - const_val
            if self.name == "day":
                max_value_DoubleVar = 4
                min = self.num - const_val - ((self.cb["val"].count(0)-1) * max_value_DoubleVar) # 2 - это пока что максимальное значение в днях =4
            else:
                max_value_DoubleVar = 2
                min = self.num - const_val - ((self.cb["val"].count(0)-1) * max_value_DoubleVar) # 2 - это пока что максимальное значение в днях =4

            if value < min and self.cb["val"].count(0) == 2:
                self.cb["StringVar"][idx].trace_vdelete('w', self.cb["StringVar"][idx].trace_id)
                self.cb["StringVar"][idx].set(str(round(min, 2)))
                self.cb["StringVar"][idx].trace_id = self.cb["StringVar"][idx].trace('w', self.magic_entry)
                value = round(min, 2)
            if value > max and self.cb["val"].count(0) == 2:
                self.cb["StringVar"][idx].trace_vdelete('w', self.cb["StringVar"][idx].trace_id)
                self.cb["StringVar"][idx].set(str(round(max, 2)))
                self.cb["StringVar"][idx].trace_id = self.cb["StringVar"][idx].trace('w', self.magic_entry)
                value = round(max, 2)
            if (value >= max or value < min):
                self.cb["StringVar"][idx].trace_vdelete('w', self.cb["StringVar"][idx].trace_id)
                # if value == max_value_DoubleVar:
                #     self.cb["StringVar"][idx].set(str(round(self.num - value - const_val, 2)))
                self.cb["StringVar"][idx].set(str(round(list_values[self.name][idx], 2)))
                self.cb["StringVar"][idx].trace_id = self.cb["StringVar"][idx].trace('w', self.magic_entry)
            else:
                # Расчёт по формуле чтобы всегда было = 1
                for i in range(self.num_day, self.num_day + self.num):
                    if i == idx:
                        x = round(self.num - value - const_val, 2)# / (self.cb["val"].count(0) - 1) # Определяем какие значения у оставшихся должны быть чтобы всё было == 1
                        z = round((x - no_const_val) / (self.cb["val"].count(0) - 1), 2)
                        # print("x = ", self.num, "-", value, "-", const_val , "=", x)
                        # print("z = (", x, "-", no_const_val, ") / (", self.cb["val"].count(0), "- 1) = ",z)
                        for index in no_const_list_index:
                            self.cb["StringVar"][index].trace_vdelete('w', self.cb["StringVar"][index].trace_id)
                            if self.cb["val"].count(0) == 2:
                                self.cb["StringVar"][index].set(str(x))
                            else:
                                rez = round(float(self.cb["StringVar"][index].get()) + z, 2)
                                self.cb["StringVar"][index].set(str(rez))
                            self.cb["StringVar"][index].trace_id = self.cb["StringVar"][index].trace('w', self.magic_entry)
                            list_values[self.name][index] = float(self.cb["StringVar"][index].get())
                        list_values[self.name][i] = float(self.cb["StringVar"][i].get())

    # def magic_round(self, value):
    #     # sleep(0.05)
    #     const_val = 0
    #     no_const_val = 0
    #     no_const_list_index = []
    #
    #     value = round(float(value), 2)
    #     # Сначала рассчитываем значение которые имеются, фиксированные и не фиксированные...
    #     for i in range(self.num_day, self.num_day + self.num):
    #         v_get = round(self.v[i].get(), 2)
    #         # print(v_get)
    #         if self.cb["val"][i] == 1:
    #             const_val += v_get
    #         else:
    #             if v_get != value:
    #                 no_const_val += v_get
    #                 no_const_list_index.append(i)
    #
    #     ### Расчет минимального и максимального значения ###
    #     max = self.num - const_val
    #     if self.name == "day":
    #         min = self.num - const_val - ((self.cb["val"].count(0)-1) * 4) # 2 - это пока что максимальное значение в днях =4
    #     else:
    #         min = self.num - const_val - ((self.cb["val"].count(0)-1) * 2) # 2 - это пока что максимальное значение в днях =4
    #
    #     # Проблема, значение уходит выше 2 при расчете.
    #     # Сделать максимальное и минимальное зназение после которого двигать нельзя!
    #     # Сделать расчет с учетом тех значений которые уже использовались.
    #
    #     if value >= max or value <= min:
    #         for i in range(self.num_day, self.num_day + self.num):
    #             if round(self.v[i].get(), 2) == value:
    #                 self.v[i].set(list_values[self.name][i])
    #     else:
    #         # Расчёт по формуле чтобы всегда было = 1
    #         for i in range(self.num_day, self.num_day + self.num):
    #             if round(self.v[i].get(), 2) == value:
    #                 x = round(self.num - value - const_val, 2)# / (self.cb["val"].count(0) - 1) # Определяем какие значения у оставшихся должны быть чтобы всё было == 1
    #                 z = round((x - no_const_val) / (self.cb["val"].count(0) - 1), 2)
    #                 print("x = ", self.num, "-", value, "-", const_val , "=", x)
    #                 print("z = (", x, "-", no_const_val, ") / (", self.cb["val"].count(0), "- 1) = ",z)
    #                 for index in no_const_list_index:
    #                     if self.cb["val"].count(0) == 2:
    #                             self.v[index].set(x)
    #                     else:
    #                         self.v[index].set(self.v[index].get()+z)
    #                     list_values[self.name][index] = self.v[index].get()
    #                 list_values[self.name][i] = self.v[i].get()
    #     # self.lable_test.config(text=str(sum(list_values[self.name])/len(list_values[self.name])))
    #
    # # def magic(self, value):
    # #     print(self.name)
    # #     print(value)
    # #     # sleep(0.05)
    # #     const_val = 0
    # #     no_const_val = 0
    # #     no_const_list_index = []
    # #
    # #     value = round(float(value), 2)
    # #     # Сначала рассчитываем значение которые имеются, фиксированные и не фиксированные...
    # #     for i in range(self.num_day, self.num_day + self.num):
    # #         v_get = round(self.v[i].get(), 2)
    # #         # print(v_get)
    # #         if self.cb["val"][i] == 1:
    # #             const_val += v_get
    # #         else:
    # #             if v_get != value:
    # #                 no_const_val += v_get
    # #                 no_const_list_index.append(i)
    # #
    # #     ### Расчет минимального и максимального значения ###
    # #     max = self.num - const_val
    # #     if self.name == "day":
    # #         min = self.num - const_val - ((self.cb["val"].count(0)-1) * 4) # 2 - это пока что максимальное значение в днях =4
    # #     else:
    # #         min = self.num - const_val - ((self.cb["val"].count(0)-1) * 2) # 2 - это пока что максимальное значение в днях =4
    # #
    # #     # Проблема, значение уходит выше 2 при расчете.
    # #     # Сделать максимальное и минимальное зназение после которого двигать нельзя!
    # #     # Сделать расчет с учетом тех значений которые уже использовались.
    # #
    # #     if value >= max or value <= min:
    # #         # Подозреваю что тут сбой
    # #         for i in range(self.num_day, self.num_day + self.num):
    # #             if round(self.v[i].get(), 2) == value:
    # #                 self.v[i].set(list_values[self.name][i])
    # #     else:
    # #         # Расчёт по формуле чтобы всегда было = 1
    # #         for i in range(self.num_day, self.num_day + self.num):
    # #             if round(self.v[i].get(), 2) == value:
    # #                 x = round(self.num - value - const_val, 2)# / (self.cb["val"].count(0) - 1) # Определяем какие значения у оставшихся должны быть чтобы всё было == 1
    # #                 z = round((x - no_const_val) / (self.cb["val"].count(0) - 1), 2)
    # #                 # print("x = ", self.num, "-", value, "-", const_val , "=", x)
    # #                 # print("z = (", x, "-", no_const_val, ") / (", self.cb["val"].count(0), "- 1) = ",z)
    # #                 for index in no_const_list_index:
    # #                     if self.cb["val"].count(0) == 2:
    # #                             self.v[index].set(x)
    # #                     else:
    # #                         self.v[index].set(self.v[index].get()+z)
    # #                     list_values[self.name][index] = self.v[index].get()
    # #                 list_values[self.name][i] = self.v[i].get()
    #
    # # Надо создать запрет на ввод чисел больше 2 и меньше 0
    # # НАдо поправить Баг с ползунками который возникает если значение ползунков совпадает, ну я там пометил...найди!
    #
    # # Проблема, значение уходит выше 2 при расчете.
    # # Сделать максимальное и минимальное зназение после которого двигать нельзя!
    # # Сделать расчет с учетом тех значений которые уже использовались.
    #
    # def magic_entry_OLD(self, idx, q='', w=''):
    #     const_val = 0
    #     no_const_val = 0
    #     no_const_list_index = []
    #     idx = int(idx)
    #     if str(self.cb["entry"][idx].get()) != "" and str(self.cb["entry"][idx].get()) != ".":
    #         value = round(float(self.cb["entry"][idx].get()), 2)
    #         self.v[idx].set(value)
    #         # Сначала рассчитываем значение которые имеются, фиксированные и не фиксированные...
    #         for i in range(self.num_day, self.num_day + self.num):
    #             v_get = round(float(self.cb["entry"][i].get()), 2)
    #             # print(v_get)
    #             if self.cb["val"][i] == 1:
    #                 const_val += v_get
    #             else:
    #                 if v_get != value:
    #                     no_const_val += v_get
    #                     no_const_list_index.append(i)
    #
    #         ### Расчет минимального и максимального значения ###
    #         max = self.num - const_val
    #         if self.name == "day":
    #             max_value_DoubleVar = 4
    #             min = self.num - const_val - ((self.cb["val"].count(0)-1) * max_value_DoubleVar) # 2 - это пока что максимальное значение в днях =4
    #         else:
    #             max_value_DoubleVar = 2
    #             min = self.num - const_val - ((self.cb["val"].count(0)-1) * max_value_DoubleVar) # 2 - это пока что максимальное значение в днях =4
    #
    #         if value < min and self.cb["val"].count(0) == 2:
    #             self.cb["StringVar"][idx].set(str(round(min, 2)))
    #             self.v[idx].set(round(min, 2))
    #             value = round(min, 2)
    #         if value > max and self.cb["val"].count(0) == 2:
    #             self.cb["StringVar"][idx].set(str(round(max, 2)))
    #             self.v[idx].set(round(max, 2))
    #             value = round(max, 2)
    #         if (value >= max or value < min):
    #             self.cb["StringVar"][idx].trace_vdelete('w', self.cb["StringVar"][idx].trace_id)
    #             # if value == max_value_DoubleVar:
    #             #     self.cb["StringVar"][idx].set(str(round(self.num - value - const_val, 2)))
    #             self.cb["StringVar"][idx].set(str(round(list_values[self.name][idx], 2)))
    #             self.v[idx].set(round(list_values[self.name][idx], 2))
    #             self.cb["StringVar"][idx].trace_id = self.cb["StringVar"][idx].trace('w', self.magic_entry)
    #         else:
    #             # Расчёт по формуле чтобы всегда было = 1
    #             for i in range(self.num_day, self.num_day + self.num):
    #                 if i == idx:
    #                     x = round(self.num - value - const_val, 2)# / (self.cb["val"].count(0) - 1) # Определяем какие значения у оставшихся должны быть чтобы всё было == 1
    #                     z = round((x - no_const_val) / (self.cb["val"].count(0) - 1), 2)
    #                     # print("x = ", self.num, "-", value, "-", const_val , "=", x)
    #                     # print("z = (", x, "-", no_const_val, ") / (", self.cb["val"].count(0), "- 1) = ",z)
    #                     for index in no_const_list_index:
    #                         self.cb["StringVar"][index].trace_vdelete('w', self.cb["StringVar"][index].trace_id)
    #                         if self.cb["val"].count(0) == 2:
    #                             self.cb["StringVar"][index].set(str(x))
    #                             self.v[index].set(x)
    #                         else:
    #                             rez = round(float(self.cb["StringVar"][index].get()) + z, 2)
    #                             self.cb["StringVar"][index].set(str(rez))
    #                             self.v[index].set(rez)
    #                         self.cb["StringVar"][index].trace_id = self.cb["StringVar"][index].trace('w', self.magic_entry)
    #                         list_values[self.name][index] = float(self.cb["StringVar"][index].get())
    #                     list_values[self.name][i] = float(self.cb["StringVar"][i].get())
    # def magic_OLD(self, value, idx=False, w=False):#
    #     # sleep(0.05)
    #     # try:
    #         const_val = 0
    #         no_const_val = 0
    #         no_const_list_index = []
    #         index=-1994
    #         # print(value)
    #         if "index=" in value:
    #             index = int(value.replace("index=",""))
    #             value = float(self.cb["entry"][index].get())
    #             idx=True
    #         else:
    #             value = float(value)
    #         # print(value)
    #         # Сначала рассчитываем значение которые имеются, фиксированные и не фиксированные...
    #         for i in range(len(list_values[self.name])):
    #             v_get = self.v[i].get()
    #             # print(v_get)
    #             if self.cb["val"][i] == 1:
    #                 const_val += v_get
    #             else:
    #                 if v_get != value:
    #                     no_const_val += v_get
    #                     no_const_list_index.append(i)
    #
    #         ### Расчет минимального и максимального значения ###
    #         max = self.num - const_val
    #         if self.name == "day":
    #             min = self.num - const_val - ((self.cb["val"].count(0)-1) * 4) # 2 - это пока что максимальное значение в днях =4
    #         else:
    #             min = self.num - const_val - ((self.cb["val"].count(0)-1) * 2) # 2 - это пока что максимальное значение в днях =4
    #
    #         # Проблема, значение уходит выше 2 при расчете.
    #         # Сделать максимальное и минимальное зназение после которого двигать нельзя!
    #         # Сделать расчет с учетом тех значений которые уже использовались.
    #
    #         if value > max or value < min:
    #             for i in range(self.num_day, self.num_day + self.num):
    #                 if self.v[i].get() == value:
    #                     self.v[i].set(list_values[self.name][i])
    #                     break
    #             if idx:
    #                 print(max)
    #                 print(min)
    #                 self.cb["StringVar"][index].trace_vdelete('w', self.cb["StringVar"][index].trace_id)
    #                 self.cb["StringVar"][index].set(self.v[index].get())
    #                 self.cb["StringVar"][index].trace_id = self.cb["StringVar"][index].trace('w', self.magic)
    #         else:
    #             if idx:
    #                 self.v[index].set(value)
    #             # Расчёт по формуле чтобы всегда было = 1
    #             for i in range(len(list_values[self.name])):
    #                 if self.v[i].get() == value:
    #                     x = len(self.cb["val"]) - value - const_val# / (self.cb["val"].count(0) - 1) # Определяем какие значения у оставшихся должны быть чтобы всё было == 1
    #                     z = (x - no_const_val) / (self.cb["val"].count(0) - 1)
    #                     if not idx:
    #                         self.cb["StringVar"][i].trace_vdelete('w', self.cb["StringVar"][i].trace_id)
    #                         self.cb["StringVar"][i].set(self.v[i].get())
    #                         self.cb["StringVar"][i].trace_id = self.cb["StringVar"][i].trace('w', self.magic)
    #                     # print("x = ", len(self.cb["val"]), "-", value, "-", const_val , "=", x)
    #                     # print("z = (", x, "-", no_const_val, ") / (", self.cb["val"].count(0), "- 1) = ",z)
    #
    #                     for index in no_const_list_index:
    #                         if self.cb["val"].count(0) == 2:
    #                                 self.v[index].set(x)
    #                                 self.cb["StringVar"][index].trace_vdelete('w', self.cb["StringVar"][index].trace_id)
    #                                 # self.cb["entry"][i].delete(0, END)
    #                                 # self.cb["entry"][i].insert(0, str(round(self.v[index].get() + z,2)))
    #                                 self.cb["StringVar"][index].set(round(x, 2))
    #                                 self.cb["StringVar"][index].trace_id = self.cb["StringVar"][index].trace('w',self.magic)
    #                         else:
    #                             self.v[index].set(self.v[index].get() + z)
    #                             self.cb["StringVar"][index].trace_vdelete('w', self.cb["StringVar"][index].trace_id)
    #                             # self.cb["entry"][i].delete(0, END)
    #                             # self.cb["entry"][i].insert(0, str(round(self.v[index].get() + z,2)))
    #                             self.cb["StringVar"][index].set(self.v[index].get() + z)
    #                             self.cb["StringVar"][index].trace_id = self.cb["StringVar"][index].trace('w', self.magic)
    #                         list_values[self.name][index] = self.v[index].get()
    #                     list_values[self.name][i] = self.v[i].get()
    #     # except TclError:
    #     #     pass
    #     # self.lable_test.config(text=str(round(sum(list_values[self.name])/len(list_values[self.name]), 3)))

    def chart(self):
        fig, ax = plt.subplots()
        plt.plot(self.list_x, self.list_y, color='red')
        fig.autofmt_xdate()
        ax.grid()
        if self.name == "day":
            plt.xlim([1, 24])
        ax.set_title(self.description)
        plt.ylabel(self.label_y)
        plt.xlabel(self.label_x)
        plt.savefig(self.file_name)

        # plt.text(0, 7, "HELLO!", fontsize=15)
        # plt.plot(range(0, 10), range(0, 10))
        plt.close()

    def default(self):
        for i in range(self.num_day, self.num_day + self.num):
            self.scale_list[i].configure(state='active')
            self.cb["entry"][i].configure(state='normal')

        for j in range(len(list_values[self.name])):
            self.cb["StringVar"][j].trace_vdelete('w', self.cb["StringVar"][j].trace_id)
            self.v[j].set(1.0)
            self.cb["box"][j].set(0)
            self.cb["val"][j] = 0
            list_values[self.name][j] = 1.0
            # self.cb["StringVar"][j].set("1.0")
            self.cb["StringVar"][j].trace_id = self.cb["StringVar"][j].trace('w', self.magic_entry)

# Данное действие необходимо иначе происходит безумие после закрытия онка и открытия другого... хоть и логично что переменные обнуляются но что-то идет не так
    def close_window(self):
        for i in range(len(self.cb["StringVar"])):
            self.cb["StringVar"][i].trace_vdelete('w', self.cb["StringVar"][i].trace_id)
            clear_window()


# Валидация ввода символов в ячейки ввода.
    def check_keys(self, text):
        list_punctuation_marks="!@#$%^&*()_-+=[{}]\|/,?><:;'\"`~ "
        # Не событие вставки или ни один символ в тексте не является буквой
        return not any(char.isalpha() for char in text) and not any(char in list_punctuation_marks for char in text)

### Дочернее приложение TKinter, открывается дочернее окно с кнопками в которых названия месяцев###
class win_setting_for_year(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Выбор месяца")
        self.resizable(width=False, height=False)

        month = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
        i = 0
        j = 0
        self.btn=[]
        self.btn.append(Button(self, text=month[0], height=5, width=10, command=lambda: self.open_month(1)))
        self.btn.append(Button(self, text=month[1], height=5, width=10, command=lambda: self.open_month(2)))
        self.btn.append(Button(self, text=month[2], height=5, width=10, command=lambda: self.open_month(3)))
        self.btn.append(Button(self, text=month[3], height=5, width=10, command=lambda: self.open_month(4)))
        self.btn.append(Button(self, text=month[4], height=5, width=10, command=lambda: self.open_month(5)))
        self.btn.append(Button(self, text=month[5], height=5, width=10, command=lambda: self.open_month(6)))
        self.btn.append(Button(self, text=month[6], height=5, width=10, command=lambda: self.open_month(7)))
        self.btn.append(Button(self, text=month[7], height=5, width=10, command=lambda: self.open_month(8)))
        self.btn.append(Button(self, text=month[8], height=5, width=10, command=lambda: self.open_month(9)))
        self.btn.append(Button(self, text=month[9], height=5, width=10, command=lambda: self.open_month(10)))
        self.btn.append(Button(self, text=month[10], height=5, width=10, command=lambda: self.open_month(11)))
        self.btn.append(Button(self, text=month[11], height=5, width=10, command=lambda: self.open_month(12)))
        # for k, name_month in enumerate(month):
        #     self.btn.append(Button(self, text=name_month, height=5, width=10, command=lambda: self.open_month(k+1)))
        for k in range(12):
            if i == 4:
                j += 1
                i = 0
            self.btn[k].grid(column=i, row=j)
            i += 1

    def open_month(self, month):
        num = int(monthrange(2022, month)[1])
        label_x = 'день'
        label_y = 'коэфф.'
        description = f"График за год"
        name = 'year'

        about = win_setting(self, num, label_x, label_y, description, name, num_month=month)
        about.grab_set()

### Очищаем основное окно, чтобы потом нарисовать новые картинки ###
def clear_window():
    for widgets in app.winfo_children():
        widgets.destroy()
    # app.__init__()
    app.main()

def main(year, num_people, q_people):
    global list_values
    # df_day = pd.read_excel(f"{os.getcwd()}/day.xlsx")
    # df_week = pd.read_excel(f"{os.getcwd()}/week.xlsx")
    # df_year = pd.read_excel(f"{os.getcwd()}/year.xlsx")

    list_day = list_values["day"]
    list_week = list_values["week"]
    list_year = list_values["year"]
    # for idx, row in df_day.iterrows():
    #     list_day.append(row['k'])
    # for idx, row in df_week.iterrows():
    #     list_week.append(row['k'])
    # for idx, row in df_year.iterrows():
    #     list_year.append(row['k'])

    rez = {
        "час": [],
        "день": [],
        "месяц": [],
        "общий расход": []
    }
    # year = 2022#int(input("Введите год цифрами, к примеру 2022\n"))#
    # num_people = 1000#int(input("Введите количество человек цифрами, к примеру 2000\n"))#
    procent = int(num_people*0.3)#10000#
    # q_people = 100/24000#int(input("Введите удельную норму водоотведения на одного жителя (л/сут), цифрами, к примеру 150\n"))/24000#
    q_people = q_people/24000#int(input("Введите удельную норму водоотведения на одного жителя (л/сут), цифрами, к примеру 150\n"))/24000#
    rezult = np.zeros(shape=(num_people, 8760))
    td = []
    # raschet(0, q_people, procent, year, list_day, list_week, list_year, rezult, rez)

    for j in range(num_people):
        app.progressbar['value'] = (j/num_people)*100
        app.label['text'] = str(round((j/num_people)*100, 1)) + "%"
        app.update_idletasks()
        t = Thread(target=raschet, args=(j, q_people, procent, year, list_day, list_week, list_year, rezult, rez,))
        t.start()
        td.append(t)
    i=0
    for t in td:
        i+=1
        app.progressbar['value'] = (i / num_people) * 100
        app.label['text'] = str(round((i / num_people) * 100, 1)) + "%"
        app.update_idletasks()
        t.join()
    rez['общий расход'] = sum(rezult).tolist()
    # list_rez = sample(rez["общий расход"], len(rez["общий расход"]))
    # rez['общий расход'] = list_rez
    # df2 = pd.DataFrame(rez).drop('месяц', axis=1).drop('день', axis=1) #Убираем ненужные колонки из датафрейма
    df = pd.DataFrame(rez)
    df.to_excel(f"{os.getcwd()}/expense_schedule.xlsx", index=None)
    app.label['text'] = "Готово!"
    app.update_idletasks()
    # df2.to_excel(f"{os.getcwd()}/expense_schedule4.xlsx", index=None)
    return df

### Общий расчет ###
def raschet(j, q_people, procent, year, list_day, list_week, list_year, rezult, rez):
    global test
    weekday = int(monthrange(year, 1)[0])  # узнаём день недели первого дня.
    hour = 1
    day_for_year = 0
    for i in range(12):
        if rand_opt:
            if j > procent:
                list_day = sample(list_day, len(list_day))
                list_week = sample(list_week, len(list_week))
            list_year = sample(list_year, len(list_year))
        month = i + 1
        days = int(monthrange(year, month)[1])  # узнаём количество дней в месяце
        for day in range(days):
            value_w = list_week[weekday]
            value_m = list_year[day_for_year]
            day_for_year += 1
            for i_h in range(24):
                value_h = list_day[i_h]
                consumption = value_h * value_w * value_m * q_people
                if rand_opt:
                    random_num = uniform((consumption * 0.15) * (-1), (consumption * 0.15))#0#
                else:
                    random_num = 0#uniform((consumption * 0.15) * (-1), (consumption * 0.15))#
                if j == 0:
                    rez["час"].append(hour)
                    rez["день"].append(day+1)
                    rez["месяц"].append(month)
                rezult[j][hour - 1] = consumption + random_num
                hour += 1
            weekday += 1
            if weekday == 7:
                weekday = 0



################################
# Расчет и сохранение графиков #
################################

### Расчет для графика "Годовой расход" ###
def chart_year(df):
    day = 1
    day_i = 1
    days = []
    value = []
    value_for_df = []
    values_vrem = []
    for idx, row in df.iterrows():
        if int(df['час'].max()) == int(row['час']):
            values_vrem.append(row["общий расход"])
            rez_velues_vrem = (sum(values_vrem) / (len(values_vrem))) * 24
            value.append(rez_velues_vrem)
            for i in range(24):
                value_for_df.append(rez_velues_vrem)
            values_vrem = []
            days.append(day_i)
        elif int(row['день']) == day:
            values_vrem.append(row["общий расход"])
        else:
            rez_velues_vrem = (sum(values_vrem) / (len(values_vrem))) * 24
            value.append(rez_velues_vrem)
            for i in range(24):
                value_for_df.append(rez_velues_vrem)
            day = int(row['день'])
            days.append(day_i)
            day_i += 1
            values_vrem = []
            values_vrem.append(row["общий расход"])
    label_x = 'день'
    label_y = 'м3/сут'
    description = f"Годовой расход, м3/сут"
    file_name = f'chart_year.jpeg'
    chart(days, value, label_x, label_y, description, file_name)
    df['for_year'] = value_for_df
    return df

### Расчет для графика "суточный расход" ###
def faind_max_min_in_day(df):
    max_min_value = [[df['for_year'].max(), 'max', 'Максимальный'], [df['for_year'].min(), 'min', 'Минимальный']]#
    for v in max_min_value:
        df2 = df[df['for_year'] == v[0]]
        for idx, row in df2.iterrows():
            df3 = df[df['месяц'] == row['месяц']]
            day = 1
            day_i = 1
            days = []
            value = []
            values_vrem = []
            for idx, row2 in df3.iterrows():
                if int(df3['час'].max()) == int(row2['час']):
                    days.append(day_i)
                    values_vrem.append(row2["общий расход"])
                    value.append((sum(values_vrem) / (len(values_vrem))) * 24)
                    values_vrem = []
                elif int(row2['день']) == day:
                    values_vrem.append(row2["общий расход"])
                else:
                    value.append((sum(values_vrem) / (len(values_vrem))) * 24)
                    day = int(row2['день'])
                    days.append(day_i)
                    day_i += 1
                    values_vrem = []
                    values_vrem.append(row2["общий расход"])
            if days != []:
                label_x = 'день'
                label_y = 'м3/сут'
                description = f"{v[2]} суточный расход, м3/сут"# ({int(row['месяц'])}й месяц)"
                file_name = f'{v[1]}_chart_month.jpeg'
                if v[1] == "max":
                    chart(days, value, label_x, label_y, description, file_name, max_point=True)
                else:
                    chart(days, value, label_x, label_y, description, file_name, min_point=True)
            break

### Расчет для графика "часовой расход" ###
def faind_max_min_in_hour(df):
    max_min_value = [[df['for_year'].max(), 'max', 'Максимальный'], [df['for_year'].min(), 'min', 'Минимальный']]
    for v in max_min_value:
        df2 = df[df['for_year'] == v[0]]
        for idx, row in df2.iterrows():
            df3 = df[df['месяц'] == row['месяц']]
            df3 = df3[df3['день'] == row['день']]
            hour = [i for i in range(1, 25)]
            value = []
            for idx, row2 in df3.iterrows():
                value.append(row2["общий расход"])
            if value != []:
                label_x = 'час'
                label_y = 'м3/час'
                description = f"{v[2]} часовой расход, м3/час"# ({int(row['день'])}й день, {int(row['месяц'])}й месяц)"
                file_name = f'{v[1]}_chart_hour.jpeg'
                if v[1] == "max":
                    chart(hour, value, label_x, label_y, description, file_name, limit=True, max_point=True)
                else:
                    chart(hour, value, label_x, label_y, description, file_name, limit=True, min_point=True)
            break

### Рисуем графики по параметрам которые присылаем ###
def chart(list_x,list_y,label_x, label_y, description, file_name, limit=False, max_point=False, min_point=False):
    fig, ax = plt.subplots()
    plt.plot(list_x, list_y)
    fig.autofmt_xdate()
    ax.grid()
    ax.set_title(description)
    # if max_point or min_point:
    #     if max_point:
    #         p = max(list_y)
    #         p2 = min(list_y)
    #         txt2 = f"max={round(p, 2)}\nmin={round(p2, 2)}\n"
    #         if "часовой расход" in description:
    #             txt = f"Kmax={round(max(list_values['day']), 2)}\nKmin={round(min(list_values['day']), 2)}\nQср={round(sum(list_y) / len(list_y), 2)}\n"
    #             txt2 = f"max={round(max(list_values['day']), 2)}\nmin={round(min(list_values['day']), 2)}\n"
    #         else:
    #             txt = f"Kmax={round(max(list_values['week']), 2)}\nKmin={round(min(list_values['week']), 2)}\nQср={round(sum(list_y) / len(list_y), 2)}\n"
    #             txt2 = f"max={round(max(list_values['week']), 2)}\nmin={round(min(list_values['week']), 2)}\n"
    #     if min_point:
    #         p2 = max(list_y)
    #         p = min(list_y)
    #         txt2 = f"max={round(p2, 2)}\nmin={round(p, 2)}\n"
    #         if "часовой расход" in description:
    #             txt = f"Kmax={round(max(list_values['day']), 2)}\nKmin={round(min(list_values['day']), 2)}\nQср={round(sum(list_y) / len(list_y), 2)}\n"
    #         else:
    #             txt = f"Kmax={round(max(list_values['week']), 2)}\nKmin={round(min(list_values['week']), 2)}\nQср={round(sum(list_y) / len(list_y), 2)}\n"
    #     p_index = list_y.index(p)
    #     # max(list_y)
    #     # ax.text(list_x[max_p_index]+0.5, max_p+0.2, str(round(max_p, 2)), fontsize=10, color='red', bbox={'boxstyle':'square', 'facecolor': '#AAAAFF'})
    #     plt.plot([list_x[p_index]], [p], 'o', color='red')
    #     plt.figtext(0.75, -0.025, txt, color='red', fontsize=10)#center,  wrap=True,
    #     plt.figtext(0.05, 0, txt2, color='red', fontsize=10)#center,  wrap=True,
    if max_point or min_point:
        p = max(list_y)
        p2 = min(list_y)
        if "часовой расход" in description:
            txt = f"Kmax={round(max(list_values['day']), 2)}\nKmin={round(min(list_values['day']), 2)}\nQср={round(sum(list_y) / len(list_y), 2)}\n"
        else:
            txt = f"Kmax={round(max(list_values['week']), 2)}\nKmin={round(min(list_values['week']), 2)}\nQср={round(sum(list_y) / len(list_y), 2)}\n"
        p_index = list_y.index(p)
        p2_index = list_y.index(p2)
        plt.plot([list_x[p_index]], [p], 'o', color='red')
        plt.plot([list_x[p2_index]], [p2], 'o', color='blue')
        plt.figtext(0.75, -0.01, txt, color='red', fontsize=10)#center,  wrap=True,
        plt.figtext(0.07, 0.07, f"max={round(p, 2)}", color='red', fontsize=10)#center,  wrap=True,
        plt.figtext(0.07, 0.035, f"min={round(p2, 2)}", color='blue', fontsize=10)#center,  wrap=True,
    plt.ylabel(label_y)
    plt.xlabel(label_x)
    if limit:
        plt.xlim([1, len(list_x)])
    plt.savefig(file_name)
    plt.close()

    def check_keys(text):
        list_punctuation_marks="!@#$%^&*()_-+=[{}]\|/,?><:;'\"`~"
        # Не событие вставки или ни один символ в тексте не является буквой
        return not any(char.isalpha() for char in text) and not any(char in list_punctuation_marks for char in text)

if __name__ == "__main__":
    app = main_app()
    app.mainloop()
