import os
import datetime
from calendar import monthrange
from random import uniform, sample
from tqdm import tqdm
from threading import Thread

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

def main():
    # print(os.getcwd())
    df_day = pd.read_excel(f"{os.getcwd()}/day.xlsx")
    df_week = pd.read_excel(f"{os.getcwd()}/week.xlsx")
    df_year = pd.read_excel(f"{os.getcwd()}/year.xlsx")
    rez = {
        "час": [],
        "коэф. за час": [],
        "коэф. за неделю": [],
        "коэф. за год": [],
        "Qчел (л/сут)": [],
        "л/сут": [],
        "рандом": [],
        "сумма": [],
        "Кол-во человек": [],
        "общий расход": []
    }
    year = 2022#int(input("Введите год цифрами, к примеру 2022\n"))
    num_people = 2000#int(input("Введите количество человек цифрами, к примеру 2000\n"))
    q_people = 150#int(input("Введите количество потребление воды одним человеком (л/сут.), цифрами, к примеру 150\n"))
    week = int(monthrange(year, 1)[0]) # узнаём день недели первого дня.
    hour = 1
    for idx, row_m in df_year.iterrows():
        month = int(row_m['month'])
        value_m = row_m['k']
        days = int(monthrange(year, month)[1])  # узнаём количество дней в месяце
        for day in range(days):
            for idx, row_h in df_day.iterrows():
                value_h = row_h['k']

                items_week = df_week[df_week['week'] == (week + 1)]
                for idx, row_w in items_week.iterrows():
                    value_w = row_w['k']
                rez["час"].append(hour)
                rez["коэф. за час"].append(value_h)
                rez["коэф. за неделю"].append(value_w)
                rez["коэф. за год"].append(value_m)
                rez["Qчел (л/сут)"].append(q_people)
                consumption = value_h * value_w * value_m * q_people
                rez["л/сут"].append(consumption)
                random_num = uniform((consumption * 0.15) * (-1), (consumption * 0.15))
                rez["рандом"].append(random_num)
                rez["сумма"].append(consumption + random_num)
                rez["Кол-во человек"].append(num_people)
                rez["общий расход"].append((consumption + random_num) * num_people)

                hour += 1
            week += 1
            if week == 7:
                week = 0
        list_rez = sample(rez["общий расход"], len(rez["общий расход"]))
        chart(list_x=rez["час"], list_y=list_rez, label_x="час", label_y="общий расход",
              description=f"Общий расзод воды за {month}й месяц.", file_name=f"general_schedule_{month}.jpeg", limit=False)

    df = pd.DataFrame(rez)
    df.to_excel(f"{os.getcwd()}/expense_schedule.xlsx", index=None)
    # print(rez["общий расход"])
    chart(list_x=rez["час"], list_y=rez["общий расход"], label_x="час", label_y="общий расход", description = "Общий расход воды за год.", file_name="general_schedule.jpeg", limit=False)
    list_x = []
    list_y = []
    label_x = 'час'
    label_y = 'коэф.'
    description = "График за 1 день"
    file_name = 'chart_day.jpeg'
    for idx, row in df_day.iterrows():
        list_y.append(row['k'])
        list_x.append(row['hour'])
    chart(list_x, list_y, label_x, label_y, description, file_name)
    list_x = []
    list_y = []
    label_x = 'номер недели'
    label_y = 'коэф.'
    description = "График за 1 неделю"
    file_name = 'chart_week.jpeg'
    for idx, row in df_week.iterrows():
        list_y.append(row['k'])
        list_x.append(row['week'])
    chart(list_x, list_y, label_x, label_y, description, file_name)
    list_x = []
    list_y = []
    label_x = 'номер месяца'
    label_y = 'коэф.'
    description = "График за год"
    file_name = 'chart_year.jpeg'
    for idx, row in df_year.iterrows():
        list_y.append(row['k'])
        list_x.append(row['month'])
    chart(list_x, list_y, label_x, label_y, description, file_name)

def main3():
    df_day = pd.read_excel(f"{os.getcwd()}/day.xlsx")
    df_week = pd.read_excel(f"{os.getcwd()}/week.xlsx")
    df_year = pd.read_excel(f"{os.getcwd()}/year.xlsx")

    list_day = []
    list_week = []
    list_year = []
    for idx, row in df_day.iterrows():
        list_day.append(row['k'])
    for idx, row in df_week.iterrows():
        list_week.append(row['k'])
    for idx, row in df_year.iterrows():
        list_year.append(row['k'])

    rez = {
        "час": [],
        "общий расход": []
    }
    year = 2022#int(input("Введите год цифрами, к примеру 2022\n"))
    num_people = 2000#int(input("Введите количество человек цифрами, к примеру 2000\n"))
    procent = int(num_people*0.3)
    q_people = 150#int(input("Введите количество потребление воды одним человеком (л/сут.), цифрами, к примеру 150\n"))
    rezult = np.zeros(shape=(procent+1, 8760))
    td = []
    for j in tqdm(range(procent+1)):
        t = Thread(target=raschet, args=(j, q_people, num_people, procent, year, df_day, df_week, df_year, list_day, list_week, list_year, rezult, rez,))
        t.start()
        td.append(t)
    for t in tqdm(td):
        t.join()
        # list_rez = sample(rez["общий расход"], len(rez["общий расход"]))
    rez['общий расход'] = sum(rezult)
    df = pd.DataFrame(rez)
    df.to_excel(f"{os.getcwd()}/expense_schedule2.xlsx", index=None)

def raschet(j, q_people, num_people, procent, year, df_day, df_week, df_year, list_day, list_week, list_year, rezult, rez):
    week = int(monthrange(year, 1)[0])  # узнаём день недели первого дня.
    hour = 1
    for i in range(len(df_year)):
        if j != 0:
            list_day = sample(list_day, len(list_day))
            list_week = sample(list_week, len(list_week))
            list_year = sample(list_year, len(list_year))
        month = i + 1
        value_m = list_year[i]
        days = int(monthrange(year, month)[1])  # узнаём количество дней в месяце
        for day in range(days):
            for i_h in range(len(df_day)):
                value_h = list_day[i_h]
                items_week = df_week[df_week['week'] == (week + 1)]
                for i_w in range(len(items_week)):
                    value_w = list_week[i_w]
                if j == 0:
                    rez["час"].append(hour)
                consumption = value_h * value_w * value_m * q_people
                random_num = uniform((consumption * 0.15) * (-1), (consumption * 0.15))
                if j != 0:
                    rezult[j][hour-1] = consumption + random_num
                else:
                    rezult[j][hour-1] = (consumption + random_num) * (num_people - procent)
                hour += 1
            week += 1
            if week == 7:
                week = 0

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

def main2():
    df = pd.read_excel(f"{os.getcwd()}/expense_schedule2.xlsx")
    num_days_in_month = {}
    year = 2022  # int(input("Введите год цифрами, к примеру 2022\n"))
    for month in range(1, 13):
        num_days_in_month.update({month: int(monthrange(year, month)[1])})  # узнаём количество дней в месяце
    month = 1
    day = 1
    hoer = 0
    general_expense_h = []
    general_expense = []
    for idx, row in df.iterrows():
        hoer += 1
        general_expense_h.append(row['общий расход'])
        if hoer == 24:
            chart([i for i in range(1, 25)], general_expense_h, label_x="час", label_y="общий расход", description=f"Общий расход воды за {day}й день {month} месяца.", file_name=f"day/{month}/general_schedule_{day}.jpeg", limit=False)
            hoer = 0
            day += 1
            general_expense.append(sum(general_expense_h)/len(general_expense_h))
            general_expense_h = []
        if num_days_in_month[month] == day-1:
            chart([i for i in range(1, int(num_days_in_month[month]) + 1)], general_expense, label_x="день", label_y="общий расход", description=f"Общий расход воды за {month}й месяц.", file_name=f"general_schedule_{month}.jpeg", limit=False)
            general_expense = []
            day = 1
            month += 1

def test_day():
    df_day = pd.read_excel(f"{os.getcwd()}/day.xlsx")
    for i in range(10):
        list_x = []
        list_y = []
        label_x = 'час'
        label_y = 'коэф.'
        description = "График за 1 день"
        file_name = f'chart_day_{i}.jpeg'
        for idx, row in df_day.iterrows():
            list_y.append(row['k'])
            list_x.append(row['hour'])
        chart(list_x, sample(list_y, len(list_y)), label_x, label_y, description, file_name)

if __name__ == "__main__":
    # main()
    main2()
    # main3()
    # test()