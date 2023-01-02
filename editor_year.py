# -*- coding: utf-8 -*-
import os
from calendar import monthrange

from tkinter import *
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


if os.path.exists(f"{os.getcwd()}/year.xlsx"):
    df_year = pd.read_excel(f"{os.getcwd()}/year.xlsx")
    list_values = df_year['k'].to_list()
else:
    list_values = np.ones(366)

v = []
num_day = 0
num = 0


def select():
    rez = {"year": [],
           "k": []
           }
    for i in range(len(list_values)):
        rez["year"].append(i+1)
        rez["k"].append(list_values[i])
    df = pd.DataFrame(rez)
    df.to_excel(f"{os.getcwd()}/year.xlsx", index=None)
    label_x = 'номер недели'
    label_y = 'каэфф.'
    description = f"График отпуска"
    file_name = 'excel_chart_year.jpeg'
    chart(rez["year"], rez["k"], label_x, label_y, description, file_name, limit=False)


def magic(self):
    global list_values, v, num_day, num
    for i in range(num_day, num_day+num):
        if v[i].get() != list_values[i]:
            z = (list_values[i]-v[i].get())/365
            for j in range(len(list_values)):
                if j!=i:
                    v[j].set(v[j].get()+z)
                list_values[j] = v[j].get()
            break
    # print(round(sum(list_values)/24,6))


def main():
    month = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь',
             'Декабрь']
    global list_values, v, num_day, num
    top = Tk()
    # top.geometry("325x360")
    # top.resizable(width=False, height=False)
    l = []
    num_month = 10
    num_day = 0
    for m in range(1, num_month):
        num = int(monthrange(2022, m)[1])
        num_day += num
    num = int(monthrange(2022, num_month)[1])
    l.append(Label(top))
    l[0].config(text=month[num_month-1])
    l[0].grid(columnspan=25, row=0)
    for i in range(len(list_values)):
        # print(i)
        v.append(DoubleVar())
        v[i].set(list_values[i])
    for i in range(num_day, num_day+num):
        # print(i)
        l.append(Label(top))
        l[i-num_day+1].config(text=str(i-num_day+1))
        Scale(top, variable=v[i], from_=2.0, to=0.0, orient=VERTICAL, resolution=0.01, bd=0, length=300, command=magic).grid(column=i-num_day, row=1)
        l[i-num_day+1].grid(column=i-num_day, row=2)

    # scale = Scale(top, variable=v, from_=2.0, to=0.0, orient=VERTICAL, resolution=0.01, label="Lower")
    # scale.pack(anchor=CENTER)

    btn = Button(top, text="Сохранить", command=select)
    # btn.pack(anchor=CENTER)
    btn.grid(columnspan=25, row=3)
    top.mainloop()

def chart(list_x,list_y,label_x, label_y, description, file_name, limit=True):
    fig, ax = plt.subplots()
    plt.plot(list_x, list_y)#, marker='.'
    fig.autofmt_xdate()
    ax.grid()
    ax.set_title(description)
    plt.ylabel(label_y)
    plt.xlabel(label_x)
    if limit:
        plt.ylim([0, 2])
    plt.savefig(file_name)
    plt.close()

def test():
    for i in range(1,5,2):
        print(i)

if __name__ in "__main__":
    main()
    # test()