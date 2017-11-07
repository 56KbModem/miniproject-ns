from tkinter import *
from tkinter import font
import api_interface

# ---- Setup main window -----
root = Tk()
root.title('NS Reisinformatie')
root.geometry('1000x750')
root.resizable(width=False, height=False)
root.configure(bg='white')

# Setup default font which has a static width for all chars
default_font = font.Font(family="Monaco", size=12)
root.option_add("*Font", default_font)

# ---- STATION INFORMATION WINDOW ----
def station_info():

	# ---- Function declaration ----
	def get_station():
    		station = station_entry.get()
    		request = api_interface.vertrek_tijden(station)

    		# Clear listboxes before new request
    		output_listbox.delete(0, END)

    		for item in request:
        		output_listbox.insert(END, '{0:<25} {1:<20} {2:<12} {3:>5}'.format(item['eind_best'], item['vertrek_tijd'], item['trein_soort'], item['rit_nr']))
	
	# Setup station window
	station = Toplevel()
	station.title('Actuele vertrektijden station')
	station.geometry('700x400')
	station.resizable(width=False, height=False)
	station.configure(background='yellow')

	# Input box
	input_box = Frame(station, height=40, width=420, bd=2, relief=SUNKEN)
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
	output_box = Frame(station, height=215, width=680, bd=2, relief=SUNKEN)
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


# ----- MAIN MENU WINDOW -----
label = Label(master=root, text='Welkom bij de Nederlandse Spoorwegen',
              font=("Courier", 44),
              width=200,
              height=2,
              background = 'blue',
              foreground = 'yellow')
label.pack()

label = Label(master=root, text='Vind de actuele vertrektijden op jouw station',
              font=("Courier", 20),
              width=200,
              height=0,
              background = 'yellow',
              foreground = 'blue')
label.pack()

button1 = Button(master=root, text='Actuele vertrektijden', command=station_info)
button1.pack(pady=11)

label = Label(master=root, text='Weten hoelaat de trein naar huis gaat?',
              font=("Courier", 20),
              width=200,
              height=0,
              background = 'blue',
              foreground = 'yellow')
label.pack()

button2 = Button(master=root, text='Reisplanner')
button2.pack(pady=13)

label = Label(master=root, text='Statistieken',
                 font=("Courier", 20),
                 width=200,
                 height=0,
                 background = 'yellow',
                 foreground = 'blue')
label.pack()

button3 = Button(master=root, text='Zoek statistieken')
button3.pack(pady=15)

label.pack()
photo = "src/img/treinstation.gif"
image = PhotoImage(file=photo)
peace = Label(master=root,
              image=image,
              height=360)
peace.pack()

root.mainloop()
