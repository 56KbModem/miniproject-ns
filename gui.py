from tkinter import *
import ns_api_test

def get_station():
    station = station_entry.get()
    request = ns_api_test.get_request(station)

    # Clear listboxes before new request
    eindb_listbox.delete(0, END)
    vertrek_listbox.delete(0, END)
    trein_listbox.delete(0, END)
    ritnummer_listbox.delete(0, END)

    for item in request:
        eindb_listbox.insert(END, item['eind_best'])
        vertrek_listbox.insert(END, item['vertrek_tijd'])
        trein_listbox.insert(END, item['trein_soort'])
        ritnummer_listbox.insert(END, item['rit_nr'])

root = Tk()
root.title('NS Reisinformatie')
root.geometry('700x400')
root.resizable(width=False, height=False)

# Input box
input_box = Frame(root, height=40, width=420, bd=2, relief=SUNKEN)
input_box.place(x=2, y=2)

# Enter Station Label
info_label = Label(input_box, text='Voer een station in: ')
info_label.place(x=10, y=5)

# Enter Station entry
station_entry = Entry(input_box)
station_entry.place(x=140, y=5)

# Entry Station submit
station_submit = Button(input_box, text='Bevestig', command=get_station)
station_submit.place(x=330, y=5)

# Eindbestemming label
eindb_label = Label(root, text='Eindbestemming')
eindb_label.place(x=10, y=50)

# Eindbestemming listbox
eindb_listbox = Listbox(root)
eindb_listbox.place(x=10, y=70)

# Vertrektijd label
vertrek_label = Label(root, text='Vertrektijd')
vertrek_label.place(x=160, y=50)

# Vertrektijd listbox
vertrek_listbox = Listbox(root, width=40)
vertrek_listbox.place(x=160, y=70)

# Trein soort label
trein_label = Label(root, text='Soort trein')
trein_label.place(x=360, y=50)

# Trein soort listbox
trein_listbox = Listbox(root)
trein_listbox.place(x=360, y=70)

# ritnummer label
ritnummer_label = Label(root, text='Ritnummer')
ritnummer_label.place(x=430, y=50)

# ritnummer listbox
ritnummer_listbox = Listbox(root)
ritnummer_listbox.place(x=430, y=70)

root.mainloop()

