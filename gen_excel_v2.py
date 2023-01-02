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
        "день": [],
        "месяц": [],
        "общий расход": []
    }
    year = 2022#int(input("Введите год цифрами, к примеру 2022\n"))#
    num_people = 1000#int(input("Введите количество человек цифрами, к примеру 2000\n"))#
    procent = int(num_people*0.3)#10000#
    q_people = 100/24000#int(input("Введите удельную норму водоотведения на одного жителя (л/сут), цифрами, к примеру 150\n"))/24000#
    rezult = np.zeros(shape=(num_people, 8760))
    td = []
    # raschet(0, q_people, procent, year, list_day, list_week, list_year, rezult, rez)

    for j in tqdm(range(num_people)):
        t = Thread(target=raschet, args=(j, q_people, procent, year, list_day, list_week, list_year, rezult, rez,))
        t.start()
        td.append(t)
    for t in tqdm(td):
        t.join()
    rez['общий расход'] = sum(rezult).tolist()
    # list_rez = sample(rez["общий расход"], len(rez["общий расход"]))
    # rez['общий расход'] = list_rez
    # df2 = pd.DataFrame(rez).drop('месяц', axis=1).drop('день', axis=1) #Убираем ненужные колонки из датафрейма
    df = pd.DataFrame(rez)
    df.to_excel(f"{os.getcwd()}/expense_schedule.xlsx", index=None)
    # df2.to_excel(f"{os.getcwd()}/expense_schedule4.xlsx", index=None)
    return df

def chart_year(df):
    day = 1
    day_i = 1
    days = []
    value = []
    values_vrem = []
    for idx, row in df.iterrows():
        if int(df['час'].max()) == int(row['час']):
            values_vrem.append(row["общий расход"])
            value.append((sum(values_vrem) / (len(values_vrem))) * 24)
            values_vrem = []
            days.append(day_i)
        elif int(row['день']) == day:
            values_vrem.append(row["общий расход"])
        else:
            value.append((sum(values_vrem) / (len(values_vrem))) * 24)
            day = int(row['день'])
            days.append(day_i)
            day_i += 1
            values_vrem = []
            values_vrem.append(row["общий расход"])
    label_x = 'день'
    label_y = 'м3/сут'
    description = f"Годовой расход, м3/сут"
    file_name = f'chart_year.jpeg'
    chart(days, value, label_x, label_y, description, file_name, limit=False)

def faind_max_min_in_day(df):
    max_min_value = [[df['общий расход'].min(), 'min', 'Минимальный']]#[df['общий расход'].max(), 'max', 'Максимальный'],
    for v in max_min_value:
        df2 = df[df['общий расход'] == v[0]]
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
                chart(days, value, label_x, label_y, description, file_name, limit=False)
            break

def faind_max_min_in_hour(df):
    max_min_value = [[df['общий расход'].max(), 'max', 'Максимальный'], [df['общий расход'].min(), 'min', 'Минимальный']]
    for v in max_min_value:
        df2 = df[df['общий расход'] == v[0]]
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
                description = f"{v[2]} суточный расход, м3/час ({int(row['день'])}й день, {int(row['месяц'])}й месяц)"
                file_name = f'{v[1]}_chart_hour.jpeg'
                chart(hour, value, label_x, label_y, description, file_name, limit=False)
            break

def raschet(j, q_people, procent, year, list_day, list_week, list_year, rezult, rez):
    weekday = int(monthrange(year, 1)[0])  # узнаём день недели первого дня.
    week = 0
    hour = 1
    for i in range(12):
        if j > procent:
            list_day = sample(list_day, len(list_day))
            list_week = sample(list_week, len(list_week))
        list_year = sample(list_year, len(list_year))
        month = i + 1
        days = int(monthrange(year, month)[1])  # узнаём количество дней в месяце
        for day in range(days):
            value_w = list_week[weekday]
            value_m = list_year[week]
            for i_h in range(24):
                value_h = list_day[i_h]
                consumption = value_h * value_w * value_m * q_people
                random_num = uniform((consumption * 0.15) * (-1), (consumption * 0.15))#0#
                if j == 0:
                    rez["час"].append(hour)
                    rez["день"].append(day+1)
                    rez["месяц"].append(month)
                rezult[j][hour - 1] = consumption + random_num
                hour += 1
            weekday += 1
            if weekday == 7:
                weekday = 0
                week += 1

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


if __name__ == "__main__":
    # df = main()
    df = pd.read_excel(f"{os.getcwd()}/expense_schedule.xlsx")
    faind_max_min_in_day(df)
    # faind_max_min_in_hour(df)
    # chart_year(df)
