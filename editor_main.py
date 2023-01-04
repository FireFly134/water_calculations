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
from tkinter.ttk import Progressbar
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from PIL import ImageTk, Image

rand_opt = False#вкл или выкл рандома

year = 2023
num_people = 1000
q_people = 100

list_values = {"day": [],
                "week": [],
                "year":  [],
               }


class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Программа для расчета потребления воды")
        self.resizable(width=False, height=False)
        if getattr(sys, 'frozen', False):
            self.application_path = sys._MEIPASS
        elif __file__:
            self.application_path = os.path.dirname(__file__)
        iconFile = 'ivea_icon.ico'
        self.iconbitmap(default=os.path.join(self.application_path, iconFile))
        self.check()
        self.main()

    def main(self):
        w = int(640/1.5)
        h = int(480/1.5)
        self.progressbar = Progressbar(self, orient=HORIZONTAL, length=400, mode='determinate')
        self.label = Label(self, text="")
        self.year = Entry(self)  # Введите год цифрами
        self.num_people = Entry(self)  # int(input("Введите количество человек цифрами, к примеру 2000\n"))#
        self.q_people = Entry(self)  # int(input("Введите удельную норму водоотведения на одного жителя (л/сут), цифрами, к примеру 150\n"))/24000#
        self.button = Button(self, text="Произвести расчет", command=self.calculations)
        self.year.insert(0, str(year))
        # self.year_lab = Label(self, text="Введите год:")#, к примеру 2022
        self.num_people.insert(0, str(num_people))
        self.num_people_lab = Label(self, text="Введите количество человек:")# цифрами, к примеру 2000"
        self.q_people.insert(0, str(q_people))
        self.q_people_lab = Label(self, text="Введите удельную норму водоотведения на одного жителя (л/сут):")#, цифрами, к примеру 150"
        # self.year.grid(column=1, row=0, sticky="w")
        # self.year_lab.grid(column=0, row=0, sticky="w")
        self.num_people.grid(column=1, row=1, sticky="w")
        self.num_people_lab.grid(column=0, row=1, sticky="w")
        self.q_people.grid(column=1, row=2, sticky="w")
        self.q_people_lab.grid(column=0, row=2, sticky="w")
        self.progressbar.grid(columnspan=3, row=4)
        self.label.grid(columnspan=3, row=5)
        self.button.grid(columnspan=3, row=6)
        self.num_people.focus_set()
        self.q_people.focus_set()
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

        self.btn.grid(columnspan=3, row=7)
        self.btn2.grid(column=0, row=3)
        self.btn3.grid(column=1, row=3)
        self.btn4.grid(column=2, row=3)
        self.button2 = Button(self, text="Произвести расчет(из эксель)", command=self.calculations2)
        self.button2.grid(columnspan=3, row=8)

    def calculations(self):
        self.label['text'] = "                       "
        self.update_idletasks()
        df = main(year=int(self.year.get()), num_people=int(self.num_people.get()), q_people=int(self.q_people.get()))
        df2 = chart_year(df)
        faind_max_min_in_day(df2)
        faind_max_min_in_hour(df2)

    def calculations2(self):
        self.label['text'] = "                       "
        self.update_idletasks()
        df = pd.read_excel(f"{os.getcwd()}/expense_schedule.xlsx")
        self.label['text'] = "40%"
        self.update_idletasks()
        df2 = chart_year(df)
        print(df2)
        self.label['text'] = "70%"
        self.update_idletasks()
        faind_max_min_in_hour(df2)
        self.label['text'] = "90%"
        self.update_idletasks()
        faind_max_min_in_day(df2)
        self.label['text'] = "Готово"
        self.update_idletasks()

    def open_window(self):
        os.system(f"explorer {os.getcwd()}")

    def open_window_day(self):
        self.save_glob()
        num = 24
        label_x = 'Час'
        label_y = 'коэфф.'
        description = f"График за день"
        name = 'day'
        about2 = win_setting(self, num, label_x, label_y, description, name)
        about2.grab_set()

    def open_window_week(self):
        self.save_glob()
        num = 7
        label_x = 'номер недели'
        label_y = 'коэфф.'
        description = f"График за неделю"
        name = 'week'

        about2 = win_setting(self, num, label_x, label_y, description, name)
        about2.grab_set()

    def open_window_year(self):
        self.save_glob()
        about2 = win_setting_for_year(self)
        about2.grab_set()

    def save_glob(self):
        global year, num_people, q_people
        year = int(self.year.get())
        num_people = int(self.num_people.get())
        q_people = int(self.q_people.get())

    def check(self):
        global list_values
        if os.path.exists(f"{os.getcwd()}/day.xlsx"):
            df_day = pd.read_excel(f"{os.getcwd()}/day.xlsx")
        else:
            df_day = pd.read_excel(os.path.join(self.application_path, "day.xlsx"))
        list_values["day"] = df_day['k'].to_list()

        if os.path.exists(f"{os.getcwd()}/week.xlsx"):
            df_week = pd.read_excel(f"{os.getcwd()}/week.xlsx")
        else:
            df_week = pd.read_excel(os.path.join(self.application_path, "week.xlsx"))
        list_values["week"] = df_week['k'].to_list()

        if os.path.exists(f"{os.getcwd()}/year.xlsx"):
            df_year = pd.read_excel(f"{os.getcwd()}/year.xlsx")
        else:
            df_year = pd.read_excel(os.path.join(self.application_path, "year.xlsx"))
        list_values["year"] = df_year['k'].to_list()

class win_setting(Toplevel):
    # global v
    global list_values
    def __init__(self, parent, num, label_x, label_y, description, name, num_month=0):
        super().__init__(parent)
        self.scale_list = []
        self.cb = {"box": [],
                   "val": []}
        self.v = []
        self.num = num
        self.num_day = 0
        self.num_month = num_month
        self.label_x = label_x
        self.label_y = label_y
        self.description = description
        self.name = name
        self.title(f"Chart_{name}")
        self.resizable(width=False, height=False)

        win_setting.protocol(self, "WM_DELETE_WINDOW", clear_window)
        self.main_class()

    def main_class(self):
        # if self.num == 24:
        #     self.geometry("1070x380")
        #     self.resizable(width=False, height=False)
        #
        # elif self.num == 7:
        #     self.geometry("325x380")
        #     self.resizable(width=False, height=False)
        #
        # else:
        #     self.resizable(width=False, height=False)

        l = []

        if self.name == "year":
            for m in range(1, self.num_month):
                num = int(monthrange(2022, m)[1])
                self.num_day += num
            for j in range(len(list_values["year"])):
                self.v.append(DoubleVar())
                self.v[j].set(list_values["year"][j])
            for i in range(self.num_day, self.num_day + self.num):
                l.append(Label(self))
                l[i - self.num_day].config(text=str(i - self.num_day + 1))
                Scale(self, variable=self.v[i], from_=2.0, to=0.0, orient=VERTICAL, resolution=0.01, bd=0, length=300,
                      command=self.magic).grid(column=i - self.num_day, row=2)
                l[i - self.num_day].grid(column=i - self.num_day, row=3)
        else:
            for i in range(self.num):
                self.cb["box"].append(IntVar())
                self.cb["val"].append(0)
                self.v.append(DoubleVar())
                self.v[i].set(list_values[self.name][i])
                l.append(Label(self))
                if self.name == "day":
                    l[i].config(text=str(i+1)+"ч.")
                else:
                    l[i].config(text=str(i + 1))
                if self.name == "day":
                    from_scale = 4.0
                else:
                    from_scale = 2.0
                Checkbutton(self, variable=self.cb["box"][i], command=self.magic_checkbox).grid(column=i, row=1, sticky="e")
                self.scale_list.append(Scale(self, variable=self.v[i], from_=from_scale, to=0.0, orient=VERTICAL, resolution=0.01, bd=0, length=300, command=self.magic))
                self.scale_list[i].grid(column=i, row=2)
                l[i].grid(column=i, row=3)

        self.button = Button(self, text="Сохранить", command=self.select)
        self.button2 = Button(self, text="Закрыть", command=clear_window)
        self.button3 = Button(self, text="Сбросить всё на единицы", command=self.default)
        # self.button4 = Button(self, text="Отменить всё", command=self.main_class)

        self.button.grid(columnspan=55, row=4)
        self.button2.grid(columnspan=55, row=5)
        self.button3.grid(columnspan=55, row=0, sticky="w")
        # self.button4.grid(columnspan=10, column=2, row=0)

    def select(self):
        if self.name == "day":
            name_column = "hour"
        elif self.name == "week":
            name_column = "week"
        else:
            name_column = "day"
        rez = {name_column: [],
               "k": []
               }
        for i in range(len(list_values[self.name])):
            rez[name_column].append(i+1)
            rez["k"].append(list_values[self.name][i])
        df = pd.DataFrame(rez)
        df.to_excel(f"{os.getcwd()}/{self.name}.xlsx", index=None)

        self.list_x = rez[name_column]
        self.list_y = rez["k"]
        self.file_name = f'excel_chart_{self.name}.jpeg'
        self.chart()

    def magic_checkbox(self):
        for i in range(self.num_day, self.num_day + self.num):
            if self.cb["box"][i].get() != self.cb["val"][i]:
                if self.cb["val"].count(0) == 2:
                    if self.cb["box"][i].get() == 1:
                        self.cb["box"][i].set(0)
                if self.cb["box"][i].get() == 0:
                    self.cb["val"][i] = 0
                else:
                    self.cb["val"][i] = 1
                    # self.scale_list[i].state(["disabled"])
                    self.scale_list[i].configure(state='disabled')
    def magic(self, value):
        # print(value)
        for i in range(self.num_day, self.num_day + self.num):
            if self.v[i].get() != list_values[self.name][i]:
                if self.name != "year":
                    if self.cb["val"].count(1) == 0:
                        z = (list_values[self.name][i]-self.v[i].get())/(self.num-1)
                    else:
                        z = (list_values[self.name][i]-self.v[i].get())/(self.cb["val"].count(0)-1)
                    for j in range(len(list_values[self.name])):
                        if j != i and self.cb["val"][j] != 1:
                            self.v[j].set(self.v[j].get() + z)
                        list_values[self.name][j] = self.v[j].get()
                else:
                    z = (list_values[self.name][i] - self.v[i].get()) / 365
                    for j in range(len(list_values[self.name])):
                        if j != i:
                            self.v[j].set(self.v[j].get() + z)
                        list_values[self.name][j] = self.v[j].get()

                break

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
        plt.close()

    def default(self):
        for j in range(len(list_values[self.name])):
            self.v[j].set(1.0)
            # self.cb["box"][j].set(0)
            # self.cb["val"][j] = 0
            list_values[self.name][j] = 1.0

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
                description = f"{v[2]} суточный расход, м3/сут ({int(row['месяц'])}й месяц)"
                file_name = f'{v[1]}_chart_month.jpeg'
                chart(days, value, label_x, label_y, description, file_name)
            break

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
                description = f"{v[2]} часовой расход, м3/час ({int(row['день'])}й день, {int(row['месяц'])}й месяц)"
                file_name = f'{v[1]}_chart_hour.jpeg'
                chart(hour, value, label_x, label_y, description, file_name, limit=True)
            break

def raschet(j, q_people, procent, year, list_day, list_week, list_year, rezult, rez):
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
            day_for_year += 1
            value_w = list_week[weekday]
            value_m = list_year[day_for_year]
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

def chart(list_x,list_y,label_x, label_y, description, file_name, limit=False):
    fig, ax = plt.subplots()
    plt.plot(list_x, list_y)
    fig.autofmt_xdate()
    ax.grid()
    ax.set_title(description)
    plt.ylabel(label_y)
    plt.xlabel(label_x)
    if limit:
        plt.xlim([1, len(list_x)])
    plt.savefig(file_name)
    plt.close()

if __name__ == "__main__":
    app = App()
    app.mainloop()