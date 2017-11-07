from tkinter import *
from tkinter import font
import json
import api_interface

# Variable settings
json_config = 'config.json'

def get_station():
    station = station_entry.get()
    request = api_interface.get_request(station)

    # Clear listboxes before new request
    output_listbox.delete(0, END)

    for item in request:
        output_listbox.insert(END, '{0:<25} {1:<20} {2:<12} {3:>5}'.format(item['eind_best'], item['vertrek_tijd'], item['trein_soort'], item['rit_nr']))

# Setup Tkinter window
root = Tk()
root.title('NS Reisinformatie')
root.geometry('700x400')
root.resizable(width=False, height=False)
root.configure(background='yellow')

# Setup default font which has a static width for all chars
default_font = font.Font(family="Monaco", size=12)
root.option_add("*Font", default_font)

# Input box
input_box = Frame(root, height=40, width=420, bd=2, relief=SUNKEN)
input_box.place(x=10, y=10)

# Enter Station Label
info_label = Label(input_box, text='Voer een station in: ')
info_label.place(x=10, y=5)

# Enter Station entry
station_entry = Entry(input_box)
station_entry.place(x=155, y=5)

# Entry Station submit
station_submit = Button(input_box, text='Bevestig', command=get_station)
station_submit.place(x=330, y=5)

# Output box
output_box = Frame(root, height=215, width=680, bd=2, relief=SUNKEN)
output_box.place(x=10, y=55)

# Eindbestemming label
eindb_label = Label(output_box, text='Eindbestemming')
eindb_label.place(x=10, y=5)

# Vertrektijd label
vertrek_label = Label(output_box, text='Vertrektijd')
vertrek_label.place(x=230, y=5)

# Soort trein label
soort_trein_label = Label(output_box, text='Soort trein')
soort_trein_label.place(x=335, y=5)

# Rit nummer label
rit_nr_label = Label(output_box, text='Rit nummer')
rit_nr_label.place(x=420, y=5)

# Scrollbar for output
scrollbar = Scrollbar(output_box)
scrollbar.place(x=651, y=25, height=173)

# Output listbox
output_listbox = Listbox(output_box, yscrollcommand = scrollbar.set ,width=80)
output_listbox.place(x=10, y=25)


root.mainloop()
