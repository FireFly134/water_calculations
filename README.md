# water_calculations

## Необходимые библиотеки для проекта

- tkinter
- pandas
- numpy
- matplotlib
- PIL

## Команда для компиляции данного чуда:
все первоначальные файлы будут храниться в корне программы будут лежать в папке "data"
Pyinstaller.exe --onefile --windowed --icon=data/ivea_icon.ico --add-data "data/ivea_icon.ico;." --add-data "data/excel_chart_day.jpeg;." --add-data "data/excel_chart_week.jpeg;." --add-data "data/excel_chart_year.jpeg;." --add-data "data/day.xlsx;." --add-data "data/week.xlsx;." --add-data "data/year.xlsx;." editor_main.py -y
перед editor_main.py можно добавить еще параметр "--name=*название файла*" 

