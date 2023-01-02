# -*- coding: utf-8 -*-
import os

from tkinter import *
import pandas as pd
from matplotlib import pyplot as plt

df_day = pd.read_excel(f"{os.getcwd()}/day.xlsx")
list_values = df_day['k'].to_list()
v = []

def select():
    rez = {"hour": [],
           "k": []
           }
    for i in range(24):
        rez["hour"].append(i+1)
        rez["k"].append(list_values[i])
    df = pd.DataFrame(rez)
    df.to_excel(f"{os.getcwd()}/day.xlsx", index=None)
    label_x = 'Час'
    label_y = 'коэфф.'
    description = f"Часовой расход за день, м3/час "
    file_name = 'excel_chart_day.jpeg'
    chart(rez["hour"], rez["k"], label_x, label_y, description, file_name, limit=False)


def magic(self):
    global list_values
    global v
    for i in range(24):
        if v[i].get() != list_values[i]:
            z = (list_values[i]-v[i].get())/23
            for j in range(24):
                if j!=i:
                    v[j].set(v[j].get()+z)
                list_values[j] = v[j].get()
            break
    # print(round(sum(list_values)/24,6))


def main():
    global v
    top = Tk()
    top.geometry("1070x360")
    top.resizable(width=False, height=False)
    l = []
    for i in range(24):
        v.append(DoubleVar())
        v[i].set(list_values[i])
        l.append(Label(top))
        l[i].config(text=str(i+1)+"ч.")
        Scale(top, variable=v[i], from_=2.0, to=0.0, orient=VERTICAL, resolution=0.01, bd=0, length=300, command=magic).grid(column=i, row=0)
        l[i].grid(column=i, row=1)
    # scale = Scale(top, variable=v, from_=2.0, to=0.0, orient=VERTICAL, resolution=0.01, label="Lower")
    # scale.pack(anchor=CENTER)

    btn = Button(top, text="Сохранить", command=select)
    # btn.pack(anchor=CENTER)
    btn.grid(columnspan=55, row=3)
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

if __name__ in "__main__":
    main()