import json
from tkinter import *
from tkinter import font

json_file = open("config.json", 'r')
json_data = json.load(json_file)
json_file.close()



root = Tk()
root.title('Statistieken')
root.geometry('1100x400')
root.resizable(width=False, height=False)
root.configure(bg='white')
default_font = font.Font(family='Monaco', size=12)
root.option_add('*Font', default_font)

root.mainloop()