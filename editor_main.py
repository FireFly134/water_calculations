"""
https://yandex.ru/search/?text=tkinter+%D0%BA%D0%B0%D0%BA+%D0%BE%D1%82%D0%BA%D1%80%D1%8B%D0%B2%D0%B0%D1%82%D1%8C+%D0%B4%D1%80%D1%83%D0%B3%D0%B8%D0%B5+%D0%BE%D0%BA%D0%BD%D0%B0+%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D1%8B&lr=114900&clid=2270455&win=410
https://pythonru.com/uroki/vsplyvajushhie-okna-tkinter-11

скролл гдя года
https://translated.turbopages.org/proxy_u/en-ru.ru.48baf219-63a34409-f8d77d32-74722d776562/https/stackoverflow.com/questions/71677889/create-a-scrollbar-to-a-full-window-tkinter-in-python
"""
# -*- coding: utf-8 -*-
import os
import sys
import json
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

list_save_day = []
list_save_week = []
list_save_year = []

setting = {
    "list_values": {"day": [],
                    "cb_day": [],
                    "week": [],
                    "cb_week": [],
                    "year":  [],
                    "cb_year":  [],
                   },

    "pathImage": {"IMG": "",
                 "IMG2": "",
                 "IMG3": ""},
    "pathDf": {"day": "",
              "week": "",
              "year": ""},

    "set_save_day": "",
    "set_save_week": "",
    "set_save_year": ""}
def check_fails():
    global setting
    application_path = ""
    if getattr(sys, 'frozen', False):  # Проверяем создаёт ли программа временные файлы
        application_path = sys._MEIPASS  # сохраняем путь до временных файлов
    elif __file__:
        application_path = os.path.dirname(__file__)  # Если временных файлов нет, а это только когда программа не скомпилированна, берем нужные файлы рядом с папкой

    if not os.path.exists(f"{os.getcwd()}/excel_chart_day.jpeg"):
        setting["pathImage"]["IMG"] = os.path.join(application_path, 'excel_chart_day.jpeg')
    else:
        setting["pathImage"]["IMG"] = os.path.join(os.getcwd(), 'excel_chart_day.jpeg')
    if not os.path.exists(f"{os.getcwd()}/excel_chart_week.jpeg"):
        setting["pathImage"]["IMG2"] = os.path.join(application_path, 'excel_chart_week.jpeg')
    else:
        setting["pathImage"]["IMG2"] = os.path.join(os.getcwd(), 'excel_chart_week.jpeg')
    if not os.path.exists(f"{os.getcwd()}/excel_chart_year.jpeg"):
        setting["pathImage"]["IMG3"] = os.path.join(application_path, 'excel_chart_year.jpeg')
    else:
        setting["pathImage"]["IMG3"] = os.path.join(os.getcwd(), 'excel_chart_year.jpeg')

    if not os.path.exists(f"{os.getcwd()}/day.xlsx"):
        setting["pathDf"]["day"] = os.path.join(application_path, 'day.xlsx')
    else:
        setting["pathDf"]["day"] = os.path.join(os.getcwd(), 'day.xlsx')
    if not os.path.exists(f"{os.getcwd()}/week.xlsx"):
        setting["pathDf"]["week"] = os.path.join(application_path, 'week.xlsx')
    else:
        setting["pathDf"]["week"] = os.path.join(os.getcwd(), 'week.xlsx')
    if not os.path.exists(f"{os.getcwd()}/year.xlsx"):
        setting["pathDf"]["year"] = os.path.join(application_path, 'year.xlsx')
    else:
        setting["pathDf"]["year"] = os.path.join(os.getcwd(), 'year.xlsx')

if os.path.exists(os.path.join(os.getcwd(), "save_file\data_setting.json")):
    with open(os.path.join(os.getcwd(), "save_file\data_setting.json"), "r") as read_file:
        setting = json.load(read_file)
else:
    check_fails()
class general_functionality():
    global list_save_day, list_save_week, list_save_year
    def __init__(self):
        super().__init__()

    def save_file(self, name, name_file):
        if name == "day":
            if name_file not in list_save_day:
                list_save_day.append(name_file)
            img_num = "IMG"
            name_column = "hour"
            description = f"График за день"
            label_x = 'Час'
            label_y = 'коэфф.'
        elif name == "week":
            if name_file not in list_save_week:
                list_save_week.append(name_file)
            img_num = "IMG2"
            name_column = "week"
            description = f"График за неделю"
            label_x = 'номер недели'
            label_y = 'коэфф.'
        else:
            if name_file not in list_save_year:
                list_save_year.append(name_file)
            img_num = "IMG3"
            name_column = "day"
            description = f"График за год"
            label_x = 'день'
            label_y = 'коэфф.'
        rez = {name_column: [],
               "k": [],
               "chekBox": []
               }
        for i in range(len(setting["list_values"][name])): #Нужно ли эта перезапись?
            rez[name_column].append(i+1)
            rez["k"].append(setting["list_values"][name][i])
            rez["chekBox"].append(setting["list_values"][f"cb_{name}"][i])
        df = pd.DataFrame(rez)
        df.to_excel(f"{os.getcwd()}/save_file/{name}/{name_file}.xlsx", index=None)
        self.chart(name, rez[name_column], rez["k"], label_x, label_y, f'excel_chart_{name_file}.jpeg', description)
        setting["pathDf"][name] = f"{os.getcwd()}/save_file/{name}/{name_file}.xlsx"
        setting["pathImage"][img_num] = f"{os.getcwd()}/save_file/{name}/excel_chart_{name_file}.jpeg"
        clear_window()
    def chart(self, name, list_x, list_y, label_x, label_y, file_name, description):
        fig, ax = plt.subplots()
        plt.plot(list_x, list_y, color='red')
        fig.autofmt_xdate()
        ax.grid()
        if name == "day":
            plt.xlim([1, 24])
        ax.set_title(description)
        plt.ylabel(label_y)
        plt.xlabel(label_x)
        plt.savefig(f"{os.getcwd()}/save_file/{name}/{file_name}")
        plt.close()


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
        self.check_list_save()
        self.check() # Проверяем на наличие около программы документов, в противном случае достаем из корня программы файлы по дефолту
        self.main() # Открываем основное окно и рисуем интерфейс.

    def main(self):
        w = int(640/1.5)
        h = int(480/1.5)
        self.num_people_StringVar = StringVar(name="num_people")
        self.q_people_StringVar = StringVar(name="q_people")
        self.center_value_day_StringVar = StringVar(name="center_value_day")
        self.num_people_StringVar.set(str(num_people))
        self.q_people_StringVar.set("100")
        self.center_value_day_StringVar.set("")
        self.num_people_StringVar.trace_id = self.num_people_StringVar.trace('w', self.calculation_of_water_consumption)
        self.q_people_StringVar.trace_id = self.q_people_StringVar.trace('w', self.calculation_of_water_consumption)
        self.center_value_day_StringVar.trace_id = self.center_value_day_StringVar.trace('w', self.calculation_of_water_consumption)
        self.progressbar = Progressbar(self, orient=HORIZONTAL, length=400, mode='determinate')
        self.label = Label(self, text="")
        self.year = Entry(self)  # Введите год цифрами
        self.num_people = Entry(self, textvariable=self.num_people_StringVar,width=20)  # Введите количество человек цифрами, к примеру 2000
        self.num_people.config(validate="key", validatecommand=(self.num_people.register(self.check_keys), '%P'))
        self.center_value_day = Entry(self, textvariable=self.center_value_day_StringVar,width=20)
        self.center_value_day.config(validate="key", validatecommand=(self.center_value_day.register(self.check_keys), '%P'))
        self.button = Button(self, text="Произвести расчет", command=self.calculations)
        self.year.insert(0, str(year))
        self.num_people_lab = Label(self, text="Введите количество человек:")# цифрами, к примеру 2000"
        self.q_people = Combobox(self, values=["80", "100", "120", "150", "200", "300", "350"], textvariable=self.q_people_StringVar,width=17)
        # self.q_people.current(1)
        # self.q_people.insert(0, str(q_people))
        self.q_people.config(validate="key", validatecommand=(self.q_people.register(self.check_keys), '%P'))
        self.q_people_lab = Label(self, text="Введите удельную норму водоотведения на одного жителя (л/сут):")#, цифрами, к примеру 150"
        self.center_value_day_lab = Label(self, text="Введите среднесуточный расход (м\u00B3/сут):")
        # self.year.grid(column=1, row=0, sticky="w")
        # self.year_lab.grid(column=0, row=0, sticky="w")
        # self.num_people.focus_set()
        # self.q_people.focus_set()
        # self.center_value_day.focus_set()
        # self.year.focus_set()

        self.img = Image.open(setting["pathImage"]["IMG"])
        self.img2 = Image.open(setting["pathImage"]["IMG2"])
        self.img3 = Image.open(setting["pathImage"]["IMG3"])
        resize_image = self.img.resize((w, h))
        self.img = ImageTk.PhotoImage(resize_image)
        resize_image = self.img2.resize((w, h))
        self.img2 = ImageTk.PhotoImage(resize_image)
        resize_image = self.img3.resize((w, h))
        self.img3 = ImageTk.PhotoImage(resize_image)
        l = Label(self)
        l2 = Label(self)
        l3 = Label(self)
        l.image = self.img
        l2.image = self.img2
        l3.image = self.img3
        l["image"] = l.image
        l2["image"] = l2.image
        l3["image"] = l3.image
        self.save_day = Combobox(self, values=list_save_day, width=60)
        self.save_week = Combobox(self, values=list_save_week, width=60)
        self.save_year = Combobox(self, values=list_save_year, width=60)
        self.save_day.set(setting["set_save_day"])
        self.save_week.set(setting["set_save_week"])
        self.save_year.set(setting["set_save_year"])
        self.btn_save_day = Button(self, text="Сохранить", command=self.save_chart_day, width=10)
        self.btn_load_day = Button(self, text="Загрузить", command=self.load_chart_day, width=10)
        self.btn_save_week = Button(self, text="Сохранить", command=self.save_chart_week, width=10)
        self.btn_load_week = Button(self, text="Загрузить", command=self.load_chart_week, width=10)
        self.btn_save_year = Button(self, text="Сохранить", command=self.save_chart_year, width=10)
        self.btn_load_year = Button(self, text="Загрузить", command=self.load_chart_year, width=10)

        self.btn = Button(self, text="Открыть папку с файлами",
                          command=self.open_window)
        self.btn2 = Button(self, text="Открыть суточный редактор", image=self.img,
                          command=self.open_window_day)
        self.btn3 = Button(self, text="Открыть недельный редактор", image=self.img2,
                           command=self.open_window_week)
        self.btn4 = Button(self, text="Открыть годовой редактор", image=self.img3,
                           command=self.open_window_year)

        self.num_people_lab.grid(columnspan=2, column=0, row=1, sticky="w")
        self.num_people.grid(columnspan=2, column=2, row=1, sticky="w")
        self.q_people_lab.grid(columnspan=2, column=0, row=2, sticky="w")
        self.q_people.grid(columnspan=2, column=2, row=2, sticky="w")
        self.center_value_day_lab.grid(columnspan=2, column=0, row=3, sticky="w")
        self.center_value_day.grid(columnspan=2, column=2, row=3, sticky="w")

        self.btn2.grid(columnspan=2, column=0, row=4)
        self.btn3.grid(columnspan=2, column=2, row=4)
        self.btn4.grid(columnspan=2, column=4, row=4)

        self.save_day.grid(columnspan=2, column=0, row=5)
        self.save_week.grid(columnspan=2, column=2, row=5)
        self.save_year.grid(columnspan=2, column=4, row=5)
        self.btn_save_day.grid(column=0, row=6, sticky="e")
        self.btn_load_day.grid(column=1, row=6, sticky="w")
        self.btn_save_week.grid(column=2, row=6, sticky="e")
        self.btn_load_week.grid(column=3, row=6, sticky="w")
        self.btn_save_year.grid(column=4, row=6, sticky="e")
        self.btn_load_year.grid(column=5, row=6, sticky="w")


        self.progressbar.grid(columnspan=6, row=7)
        self.label.grid(columnspan=6, row=8)
        self.button.grid(columnspan=6, row=9)
        self.btn.grid(columnspan=6, row=10)
        # self.button2 = Button(self, text="Произвести расчет(из эксель)", command=self.calculations2)
        # self.button2.grid(columnspan=3, row=8)

    def calculation_of_water_consumption(self,q,w,e):#qwe переменные необходимые для работы StringVar()
        if q == "center_value_day":
            if self.num_people_StringVar.get() != "" and self.center_value_day_StringVar.get() != "":
                self.q_people_StringVar.trace_vdelete("w", self.q_people_StringVar.trace_id)
                self.q_people_StringVar.set(str(int(int(self.center_value_day_StringVar.get())*1000/int(self.num_people_StringVar.get()))))
                self.q_people_StringVar.trace_id = self.q_people_StringVar.trace("w", self.calculation_of_water_consumption)
        else:
            if self.num_people_StringVar.get() != "" and self.q_people_StringVar.get() != "":
                self.center_value_day_StringVar.trace_vdelete("w", self.center_value_day_StringVar.trace_id)
                self.center_value_day_StringVar.set(str(int(int(self.num_people_StringVar.get())*int(self.q_people_StringVar.get())/1000)))
                self.center_value_day_StringVar.trace_id = self.center_value_day_StringVar.trace("w", self.calculation_of_water_consumption)


    def calculations(self):
        self.label['text'] = "                       "
        self.update_idletasks()
        df = main(year=int(self.year.get()), num_people=int(self.num_people.get()), q_people=int(self.q_people.get()))
        df2 = chart_year(df)
        faind_max_min_in_day(df2)
        faind_max_min_in_hour(df2)

    def open_window(self):
        # os.system(f"explorer {os.getcwd()}")
        os.system(f"explorer {os.path.join(os.getcwd(), 'calculation results')}")

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

    def open_window_ask_save(self, name, name_file):
        about = win_ask_saving(self, name, name_file)
        about.grab_set()

# тут мы просто сохраняем глобальные переменные...
    def save_glob(self):
        global year, num_people, q_people
        year = int(self.year.get())
        num_people = int(self.num_people.get())
        q_people = int(self.q_people.get())

# Проверка на наличие необходимых файлов и их открытие.
    def check(self):
        global setting
        df_day = pd.read_excel(setting["pathDf"]["day"])
        df_week = pd.read_excel(setting["pathDf"]["week"])
        df_year = pd.read_excel(setting["pathDf"]["year"])

        setting["list_values"]["day"] = df_day['k'].to_list()
        setting["list_values"]["week"] = df_week['k'].to_list()
        setting["list_values"]["year"] = df_year['k'].to_list()

        setting["list_values"]["cb_day"] = df_day['chekBox'].to_list()
        setting["list_values"]["cb_week"] = df_week['chekBox'].to_list()
        setting["list_values"]["cb_year"] = df_year['chekBox'].to_list()

    # Валидация ввода символов в ячейки ввода.
    def check_keys(self, text):
        list_punctuation_marks="!@#$%^&*()_-+=[{}]\|/,?><:;'\"`~ "
        # Не событие вставки или ни один символ в тексте не является буквой
        return not any(char.isalpha() for char in text) and not any(char in list_punctuation_marks for char in text)


    def save_chart_day(self):
        setting["set_save_day"] = self.save_day.get()
        if self.save_day.get().replace(" ", "") != "":
            if os.path.exists(f"{os.getcwd()}/save_file/day"):
                if os.path.exists(f"{os.getcwd()}/save_file/day/{setting['set_save_day']}.xlsx"):
                    self.open_window_ask_save("day", setting["set_save_day"])
                else:
                    general_functionality().save_file("day", setting["set_save_day"])
            else:
                os.mkdir(f"{os.getcwd()}/save_file/day")

        # pass
    def save_chart_week(self):
        setting["set_save_week"] = self.save_week.get()
        if self.save_week.get().replace(" ", "") != "":
            if os.path.exists(f"{os.getcwd()}/save_file/week"):
                if os.path.exists(f"{os.getcwd()}/save_file/week/{setting['set_save_week']}.xlsx"):
                    self.open_window_ask_save("week", setting["set_save_week"])
                else:
                    general_functionality().save_file("week", setting["set_save_week"])
            else:
                os.mkdir(f"{os.getcwd()}/save_file/week")

        # pass
    def save_chart_year(self):
        setting["set_save_year"] = self.save_year.get()
        if self.save_year.get().replace(" ", "") != "":
            if os.path.exists(f"{os.getcwd()}/save_file/year"):
                if os.path.exists(f"{os.getcwd()}/save_file/year/{setting['set_save_year']}.xlsx"):
                    self.open_window_ask_save("year", setting["set_save_year"])
                else:
                    general_functionality().save_file("year", setting["set_save_year"])
            else:
                os.mkdir(f"{os.getcwd()}/save_file/year")

    def load_chart_day(self):
        global setting
        if os.path.exists(os.path.join(os.getcwd(), f"save_file/day/{self.save_day.get()}.xlsx")) and os.path.exists(os.path.join(os.getcwd(), f"save_file/day/excel_chart_{self.save_day.get()}.jpeg")):
            setting["pathDf"]["day"] = f"{os.getcwd()}/save_file/day/{self.save_day.get()}.xlsx"
            setting["pathImage"]["IMG"] = f"{os.getcwd()}/save_file/day/excel_chart_{self.save_day.get()}.jpeg"
            setting["set_save_day"] = self.save_day.get()
            clear_window()
    def load_chart_week(self):
        global setting
        if os.path.exists(os.path.join(os.getcwd(), f"save_file/week/{self.save_week.get()}.xlsx")) and os.path.exists(os.path.join(os.getcwd(), f"save_file/week/excel_chart_{self.save_week.get()}.jpeg")):
            setting["pathDf"]["week"] = f"{os.getcwd()}/save_file/week/{self.save_week.get()}.xlsx"
            setting["pathImage"]["IMG2"] = f"{os.getcwd()}/save_file/week/excel_chart_{self.save_week.get()}.jpeg"
            setting["set_save_week"] = self.save_week.get()
            clear_window()
    def load_chart_year(self):
        global setting
        if os.path.exists(os.path.join(os.getcwd(), f"save_file/year/{self.save_year.get()}.xlsx")) and os.path.exists(os.path.join(os.getcwd(), f"save_file/year/excel_chart_{self.save_year.get()}.jpeg")):
            setting["pathDf"]["year"] = f"{os.getcwd()}/save_file/year/{self.save_year.get()}.xlsx"
            setting["pathImage"]["IMG3"] = f"{os.getcwd()}/save_file/year/excel_chart_{self.save_year.get()}.jpeg"
            setting["set_save_year"] = self.save_year.get()
            clear_window()


    # def save_file(self, name, name_file):
    #     if name == "day":
    #         if name_file not in self.list_save_day:
    #             self.list_save_day.append(name_file)
    #         img_num = "IMG"
    #         name_column = "hour"
    #         description = f"График за день"
    #         label_x = 'Час'
    #         label_y = 'коэфф.'
    #     elif name == "week":
    #         if name_file not in self.list_save_week:
    #             self.list_save_week.append(name_file)
    #         img_num = "IMG2"
    #         name_column = "week"
    #         description = f"График за неделю"
    #         label_x = 'номер недели'
    #         label_y = 'коэфф.'
    #     else:
    #         if name_file not in self.list_save_year:
    #             self.list_save_year.append(name_file)
    #         img_num = "IMG3"
    #         name_column = "day"
    #         description = f"График за год"
    #         label_x = 'день'
    #         label_y = 'коэфф.'
    #     rez = {name_column: [],
    #            "k": [],
    #            "chekBox": []
    #            }
    #     for i in range(len(setting["list_values"][name])): #Нужно ли эта перезапись?
    #         rez[name_column].append(i+1)
    #         rez["k"].append(setting["list_values"][name][i])
    #         rez["chekBox"].append(setting["list_values"][f"cb_{name}"][i])
    #     df = pd.DataFrame(rez)
    #     df.to_excel(f"{os.getcwd()}/save_file/{name}/{name_file}.xlsx", index=None)
    #     self.chart(name, rez[name_column], rez["k"], label_x, label_y, f'excel_chart_{name_file}.jpeg', description)
    #     setting["pathDf"][name] = f"{os.getcwd()}/save_file/{name}/{name_file}.xlsx"
    #     setting["pathImage"][img_num] = f"{os.getcwd()}/save_file/{name}/excel_chart_{name_file}.jpeg"
    #     clear_window()
    # def chart(self, name, list_x, list_y, label_x, label_y, file_name, description):
    #     fig, ax = plt.subplots()
    #     plt.plot(list_x, list_y, color='red')
    #     fig.autofmt_xdate()
    #     ax.grid()
    #     if name == "day":
    #         plt.xlim([1, 24])
    #     ax.set_title(description)
    #     plt.ylabel(label_y)
    #     plt.xlabel(label_x)
    #     plt.savefig(f"{os.getcwd()}/save_file/{name}/{file_name}")
    #     plt.close()

    def check_list_save(self):
        global list_save_day, list_save_week, list_save_year
        if not os.path.exists(f"{os.getcwd()}/save_file/"):
            os.mkdir(f"{os.getcwd()}/save_file")
        if not os.path.exists(f"{os.getcwd()}/save_file/day"):
            os.mkdir(f"{os.getcwd()}/save_file/day")
        if not os.path.exists(f"{os.getcwd()}/save_file/week"):
            os.mkdir(f"{os.getcwd()}/save_file/week")
        if not os.path.exists(f"{os.getcwd()}/save_file/year"):
            os.mkdir(f"{os.getcwd()}/save_file/year")
        list_save_day = [name.replace(".xlsx", "") for name in os.listdir(f"{os.getcwd()}/save_file/day") if "excel_chart_" not in name]
        list_save_week = [name.replace(".xlsx", "") for name in os.listdir(f"{os.getcwd()}/save_file/week") if "excel_chart_" not in name]
        list_save_year = [name.replace(".xlsx", "") for name in os.listdir(f"{os.getcwd()}/save_file/year") if "excel_chart_" not in name]
class win_setting(Toplevel):
    global setting
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
            for j in range(len(setting["list_values"]["year"])):
                # Создаём чекбокс
                self.cb["box"].append(IntVar())
                self.cb["box"][j].set(setting["list_values"]["cb_year"][j])

                self.cb["val"].append(setting["list_values"]["cb_year"][j])  # Вопрос в том, можно ли обойтись без этого?

                # Создаём ползунок и помещаем туда значение
                self.v.append(DoubleVar(name=str(j)))
                self.v[j].set(setting["list_values"]["year"][j])

                # Создаём переменную для хранения значений с ячейки для ввода и реагирующую на изменения
                self.cb["StringVar"].append(StringVar(name=str(j)))  # (name=f"index={i}"))

            for i in range(self.num_day, self.num_day + self.num):
                l.append(Label(self))
                l[i - self.num_day].config(text=str(i - self.num_day + 1))
                Checkbutton(self, variable=self.cb["box"][i], command=self.magic_checkbox).grid(column=i - self.num_day, row=1,sticky="e")
                self.scale_list.append(Scale(self, variable=self.v[i], from_=2.0, to=0.0, orient=VERTICAL, resolution=0.01, bd=0, length=300))#, command=self.magic
                self.scale_list[i - self.num_day].grid(column=i - self.num_day, row=3)
                l[i - self.num_day].grid(column=i - self.num_day, row=2)

                if self.cb["val"][i] == 1:
                    self.scale_list[i - self.num_day].configure(state='disabled')
                self.cb["entry"].append(Entry(self, width=5, textvariable=self.cb["StringVar"][i]))
                self.cb["entry"][i - self.num_day].config(validate="key",validatecommand=(self.cb["entry"][i - self.num_day].register(self.check_keys), '%P'))
                self.cb["entry"][i - self.num_day].grid(column=i - self.num_day, row=4)

            for i in range(self.num_day, self.num_day + self.num):
                # self.cb["StringVar"][i].set(round(float(setting["list_values"][self.name][i]), 2))
                self.cb["StringVar"][i].trace_id = self.cb["StringVar"][i].trace('w', self.magic_entry)
        else:
            for i in range(self.num):
                # Создаём чекбокс
                self.cb["box"].append(IntVar())
                self.cb["box"][i].set(setting["list_values"][f"cb_{self.name}"][i])

                # Создаём ползунок и помещаем туда значение
                self.v.append(DoubleVar(name=str(i)))
                self.v[i].set(setting["list_values"][self.name][i])

                # Создаём переменную для хранения значений с ячейки для ввода и реагирующую на изменения
                self.cb["StringVar"].append(StringVar(name=str(i)))#(name=f"index={i}"))
                # self.cb["StringVar"][i].set(round(float(setting["list_values"][self.name][i]), 2))
                # self.cb["StringVar"][i].trace_id = self.cb["StringVar"][i].trace('w', self.magic_entry)


                self.cb["val"].append(setting["list_values"][f"cb_{self.name}"][i]) # Вопрос в том, можно ли обойтись без этого?

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
                # self.cb["StringVar"][i].set(round(setting["list_values"][self.name][i], 2))
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
            img_num = "IMG"
            name_column = "hour"
        elif self.name == "week":
            img_num = "IMG2"
            name_column = "week"
        else:
            img_num = "IMG3"
            name_column = "day"
        rez = {name_column: [],
               "k": [],
               "chekBox": []
               }
        for i in range(len(setting["list_values"][self.name])): #Нужно ли эта перезапись?
            rez[name_column].append(i+1)
            rez["k"].append(setting["list_values"][self.name][i])
            rez["chekBox"].append(self.cb["val"][i])
        df = pd.DataFrame(rez)
        df.to_excel(f"{os.getcwd()}/{self.name}.xlsx", index=None)

        self.list_x = rez[name_column]
        self.list_y = rez["k"]
        self.file_name = f'excel_chart_{self.name}.jpeg'

        setting["pathDf"][self.name] = f"{os.getcwd()}/{self.name}.xlsx"
        setting["pathImage"][img_num] = f"{os.getcwd()}/excel_chart_{self.name}.jpeg"
        setting[f"set_save_{self.name}"] = ""

        self.chart()

# отвечает за функционал черкбоксов, отслеживает было ли сделано действие и какое.
    def magic_checkbox(self):
        # Перебираем все значения
        for i in range(self.num_day, self.num_day + self.num):
            # Если значение отличается от того какое у нас было записано, то выполняем действие.
            if self.cb["box"][i].get() != self.cb["val"][i]:
                self.cb["StringVar"][i].trace_vdelete('w', self.cb["StringVar"][i].trace_id)
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
                self.cb["StringVar"][i].trace_id = self.cb["StringVar"][i].trace('w', self.magic_entry)

    def magic_entry(self, idx, q='', w=''):
        const_val = 0
        no_const_val = 0
        no_const_list_index = []
        idx = int(idx)
        if str(self.cb["StringVar"][idx].get()) != "" and str(self.cb["StringVar"][idx].get()) != ".":
            # value = round(float(self.cb["StringVar"][idx].get()), 2)
            # value = float(self.cb["StringVar"][idx].get())
            value = self.v[idx].get()
            # Сначала рассчитываем значение которые имеются, фиксированные и не фиксированные...
            # for i in range(self.num_day, self.num_day + self.num):
            for i in range(len(setting["list_values"][self.name])):
                # v_get = round(float(self.cb["StringVar"][i].get()), 2)
                v_get = float(self.cb["StringVar"][i].get())
                if self.cb["val"][i] == 1:
                    const_val += v_get
                else:
                    if idx != i:
                        no_const_val += v_get
                        no_const_list_index.append(i)

            ### Расчет минимального и максимального значения ###
            # max = self.num - const_val
            max = len(setting["list_values"][self.name]) - const_val
            if self.name == "day":
                max_value_DoubleVar = 4
                min = self.num - const_val - ((self.cb["val"].count(0)-1) * max_value_DoubleVar) # 2 - это пока что максимальное значение в днях =4
            else:
                max_value_DoubleVar = 2
                min = self.num - const_val - ((self.cb["val"].count(0)-1) * max_value_DoubleVar) # 2 - это пока что максимальное значение в днях =4

            if value < min and self.cb["val"].count(0) == 2:
                self.cb["StringVar"][idx].trace_vdelete('w', self.cb["StringVar"][idx].trace_id)
                # self.cb["StringVar"][idx].set(str(round(min, 2)))
                self.cb["StringVar"][idx].set(str(min))
                self.cb["StringVar"][idx].trace_id = self.cb["StringVar"][idx].trace('w', self.magic_entry)
                # value = round(min, 2)
                value = min
            if value > max and self.cb["val"].count(0) == 2:
                self.cb["StringVar"][idx].trace_vdelete('w', self.cb["StringVar"][idx].trace_id)
                # self.cb["StringVar"][idx].set(str(round(max, 2)))
                self.cb["StringVar"][idx].set(str(max))
                self.cb["StringVar"][idx].trace_id = self.cb["StringVar"][idx].trace('w', self.magic_entry)
                # value = round(max, 2)
                value = max
            if (value >= max or value < min):
                self.cb["StringVar"][idx].trace_vdelete('w', self.cb["StringVar"][idx].trace_id)
                # if value == max_value_DoubleVar:
                #     self.cb["StringVar"][idx].set(str(round(self.num - value - const_val, 2)))
                # self.cb["StringVar"][idx].set(str(round(setting["list_values"][self.name][idx], 2)))
                self.cb["StringVar"][idx].set(str(setting["list_values"][self.name][idx]))
                self.cb["StringVar"][idx].trace_id = self.cb["StringVar"][idx].trace('w', self.magic_entry)
            else:
                # Расчёт по формуле чтобы всегда было = 1
                # for i in range(self.num_day, self.num_day + self.num):
                #     if i == idx:
                # x = round(len(setting["list_values"][self.name]) - value - const_val, 2)#self.num / (self.cb["val"].count(0) - 1) # Определяем какие значения у оставшихся должны быть чтобы всё было == 1
                x = len(setting["list_values"][self.name]) - value - const_val#self.num / (self.cb["val"].count(0) - 1) # Определяем какие значения у оставшихся должны быть чтобы всё было == 1
                # z = round((x - no_const_val) / (self.cb["val"].count(0) - 1), 2)
                z = (x - no_const_val) / (self.cb["val"].count(0) - 1)
                # print("max=",max)
                # print("min=",min)
                # print("x = ", len(setting["list_values"][self.name]), "-", value, "-", const_val , "=", x)
                # print("z = (", x, "-", no_const_val, ") / (", self.cb["val"].count(0), "- 1) = ",z)
                for index in no_const_list_index:
                    if self.num_day <= index and index < self.num_day + self.num:
                        self.cb["StringVar"][index].trace_vdelete('w', self.cb["StringVar"][index].trace_id)
                    # rez = round(float(self.cb["StringVar"][index].get()) + z, 2)
                    rez = float(self.cb["StringVar"][index].get()) + z
                    self.cb["StringVar"][index].set(str(rez))
                    if self.num_day <= index and index < self.num_day + self.num:
                        self.cb["StringVar"][index].trace_id = self.cb["StringVar"][index].trace('w', self.magic_entry)
                    setting["list_values"][self.name][index] = float(self.cb["StringVar"][index].get())
                setting["list_values"][self.name][idx] = float(self.cb["StringVar"][idx].get())
    # def magic_entry(self, idx, q='', w=''):
    #     const_val = 0
    #     no_const_val = 0
    #     no_const_list_index = []
    #     idx = int(idx)
    #     if str(self.cb["StringVar"][idx].get()) != "" and str(self.cb["StringVar"][idx].get()) != ".":
    #         # value = round(float(self.cb["StringVar"][idx].get()), 2)
    #         # value = float(self.cb["StringVar"][idx].get())
    #         value = self.v[idx].get()
    #         # Сначала рассчитываем значение которые имеются, фиксированные и не фиксированные...
    #         # for i in range(self.num_day, self.num_day + self.num):
    #         for i in range(len(setting["list_values"][self.name])):
    #             # v_get = round(float(self.cb["StringVar"][i].get()), 2)
    #             v_get = float(setting["list_values"][self.name][i])
    #             if self.cb["val"][i] == 1:
    #                 const_val += v_get
    #             else:
    #                 if idx != i:
    #                     no_const_val += v_get
    #                     no_const_list_index.append(i)
    #
    #         ### Расчет минимального и максимального значения ###
    #         # max = self.num - const_val
    #         max = len(setting["list_values"][self.name]) - const_val
    #         if self.name == "day":
    #             max_value_DoubleVar = 4
    #             min = self.num - const_val - ((self.cb["val"].count(0)-1) * max_value_DoubleVar) # 2 - это пока что максимальное значение в днях =4
    #         else:
    #             max_value_DoubleVar = 2
    #             min = self.num - const_val - ((self.cb["val"].count(0)-1) * max_value_DoubleVar) # 2 - это пока что максимальное значение в днях =4
    #
    #         if value < min and self.cb["val"].count(0) == 2:
    #             self.cb["StringVar"][idx].trace_vdelete('w', self.cb["StringVar"][idx].trace_id)
    #             # self.cb["StringVar"][idx].set(str(round(min, 2)))
    #             self.cb["StringVar"][idx].set(str(round(min,2)))
    #             setting["list_values"][self.name][idx]=min
    #             self.cb["StringVar"][idx].trace_id = self.cb["StringVar"][idx].trace('w', self.magic_entry)
    #             # value = round(min, 2)
    #             value = min
    #         if value > max and self.cb["val"].count(0) == 2:
    #             self.cb["StringVar"][idx].trace_vdelete('w', self.cb["StringVar"][idx].trace_id)
    #             # self.cb["StringVar"][idx].set(str(round(max, 2)))
    #             self.cb["StringVar"][idx].set(str(round(max, 2)))
    #             setting["list_values"][self.name][idx] = max
    #             self.cb["StringVar"][idx].trace_id = self.cb["StringVar"][idx].trace('w', self.magic_entry)
    #             # value = round(max, 2)
    #             value = max
    #         if (value >= max or value < min):
    #             self.cb["StringVar"][idx].trace_vdelete('w', self.cb["StringVar"][idx].trace_id)
    #             self.cb["StringVar"][idx].set(str(round(float(setting["list_values"][self.name][idx]), 2)))
    #             setting["list_values"][self.name][idx] = float(setting["list_values"][self.name][idx])
    #             self.cb["StringVar"][idx].trace_id = self.cb["StringVar"][idx].trace('w', self.magic_entry)
    #         else:
    #             x = len(setting["list_values"][self.name]) - value - const_val#self.num / (self.cb["val"].count(0) - 1) # Определяем какие значения у оставшихся должны быть чтобы всё было == 1
    #             z = (x - no_const_val) / (self.cb["val"].count(0) - 1)
    #             for index in no_const_list_index:
    #                 if self.num_day <= index and index < self.num_day + self.num:
    #                     self.cb["StringVar"][index].trace_vdelete('w', self.cb["StringVar"][index].trace_id)
    #                 # rez = round(float(self.cb["StringVar"][index].get()) + z, 2)
    #                 rez = float(self.cb["StringVar"][index].get()) + z
    #                 self.cb["StringVar"][index].set(str(round(rez, 2)))
    #                 setting["list_values"][self.name][index] = rez
    #                 if self.num_day <= index and index < self.num_day + self.num:
    #                     self.cb["StringVar"][index].trace_id = self.cb["StringVar"][index].trace('w', self.magic_entry)
    #                 # setting["list_values"][self.name][index] = float(self.cb["StringVar"][index].get())
    #             # setting["list_values"][self.name][idx] = float(self.cb["StringVar"][idx].get())

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
        # if not os.path.exists(f"{os.getcwd()}/calculation results"):
        #     os.mkdir(f"{os.getcwd()}/calculation results")
        # plt.savefig(f"{os.getcwd()}/calculation results/{self.file_name}")
        plt.savefig(self.file_name)


        # plt.text(0, 7, "HELLO!", fontsize=15)
        # plt.plot(range(0, 10), range(0, 10))
        plt.close()

    def default(self):
        for i in range(self.num):
            self.scale_list[i].configure(state='active')
            self.cb["entry"][i].configure(state='normal')

        for j in range(len(setting["list_values"][self.name])):
            if self.num_day <= j and j < self.num_day + self.num:
                self.cb["StringVar"][j].trace_vdelete('w', self.cb["StringVar"][j].trace_id)
            self.v[j].set(1.0)
            self.cb["box"][j].set(0)
            self.cb["val"][j] = 0
            setting["list_values"][self.name][j] = 1.0
            # self.cb["StringVar"][j].set("1.0")
            if j >= self.num_day and j <= self.num_day + self.num:
                self.cb["StringVar"][j].trace_id = self.cb["StringVar"][j].trace('w', self.magic_entry)

# Данное действие необходимо иначе происходит безумие после закрытия онка и открытия другого... хоть и логично что переменные обнуляются но что-то идет не так
    def close_window(self):
        # for i in range(len(self.cb["StringVar"])):
        for i in range(self.num_day, self.num_day + self.num):
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

class win_ask_saving(Toplevel):
    def __init__(self, parent, name, name_file):
        super().__init__(parent)
        self.title("Выбор месяца")
        self.resizable(width=False, height=False)
        self.name = name
        self.name_file = name_file

        # win_ask_saving.protocol(self, "WM_DELETE_WINDOW", self.close_window)
        Label(self, text=f"\nФайл с названием \"{name_file}\", уже существует.\nВы действительно хотите перезаписать файл?\n").grid(columnspan=4, row=0)
        Button(self, text="Да", width=10, command=self.response_processing).grid(column=1, row=1)
        Button(self, text="Нет", width=10, command=self.destroy).grid(column=2, row=1)
        Label(self).grid(columnspan=4, row=2)

    def response_processing(self):
        general_functionality().save_file(self.name, self.name_file)

### Очищаем основное окно, чтобы потом нарисовать новые картинки ###
def clear_window():
    with open(os.path.join(os.getcwd(), "save_file\data_setting.json"), "w") as write_file:
        json.dump(setting, write_file)
    for widgets in app.winfo_children():
        widgets.destroy()
    # app.__init__()
    app.main()

def main(year, num_people, q_people):
    global setting

    list_day = setting["list_values"]["day"]
    list_week = setting["list_values"]["week"]
    list_year = setting["list_values"]["year"]

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
    if max_point or min_point:
        p = max(list_y)
        p2 = min(list_y)
        if "часовой расход" in description:
            txt = f"Kmax={round(max(setting['list_values']['day']), 2)}\nKmin={round(min(setting['list_values']['day']), 2)}\nQср={round(sum(list_y) / len(list_y), 2)}\n"
        else:
            txt = f"Kmax={round(max(setting['list_values']['week']), 2)}\nKmin={round(min(setting['list_values']['week']), 2)}\nQср={round(sum(list_y) / len(list_y), 2)}\n"
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
    if not os.path.exists(f"{os.getcwd()}/calculation results"):
        os.mkdir(f"{os.getcwd()}/calculation results")
    plt.savefig(f"{os.getcwd()}/calculation results/{file_name}")

    plt.close()

    # def check_keys(text):
    #     list_punctuation_marks="!@#$%^&*()_-+=[{}]\|/,?><:;'\"`~"
    #     # Не событие вставки или ни один символ в тексте не является буквой
    #     return not any(char.isalpha() for char in text) and not any(char in list_punctuation_marks for char in text)

if __name__ == "__main__":
    app = main_app()
    app.mainloop()
