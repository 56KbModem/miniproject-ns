from tkinter import *
from tkinter import font
import api_interface
import json

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

	# ---- Request station info ----
	def get_station():
		station = station_entry.get()
		request = api_interface.vertrek_tijden(station)

    		# Clear listboxes before new request
		output_listbox.delete(0, END)

		for item in request:
			if item['vertraging'] == '0 min':
				colour = 'white'
			else:
				colour = 'red'
			output_listbox.insert(END, '{0:<25} {1:<20} {2:<20} {3:>5} {4:>10}'.format(item['eind_best'], item['vertrek_tijd'], item['trein_soort'], item['rit_nr'], item['vertraging']))
			output_listbox.itemconfig(END, bg=colour, fg='black')

	# Setup station window
	station = Toplevel()
	station.title('NS Actuele vertrektijden')
	station.geometry('700x285')
	station.resizable(width=False, height=False)
	station.configure(background='yellow')

	# Input box
	input_box = Frame(station, height=40, width=420, bd=2, relief=SUNKEN, bg='blue')
	input_box.place(x=10, y=10)

	# Enter Station Label
	info_label = Label(input_box, bg='blue', fg='yellow', text='Voer een station in: ')
	info_label.place(x=5, y=7)

	# Enter Station entry
	station_entry = Entry(input_box, highlightbackground='blue')
	station_entry.place(x=150, y=5)

	# Entry Station submit
	station_submit = Button(input_box, text='Bevestig', command=get_station, highlightbackground='blue')
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
	rit_nr_label.place(x=465, y=5)

	# Vertraging label
	vertraging_label = Label(output_box, text='Vertraging')
	vertraging_label.place(x=555, y=5)

	# Scrollbar for output
	scrollbar = Scrollbar(output_box)
	scrollbar.place(x=651, y=25, height=173)

	# Output listbox
	output_listbox = Listbox(output_box, yscrollcommand = scrollbar.set ,width=90)
	output_listbox.place(x=10, y=25)

# ----- REISPLANNER WINDOW -----
def reisplanner():
	# Setup reisplanner window
	planner = Toplevel()
	planner.title('NS Reisplanner')
	planner.geometry('572x360')
	planner.resizable(width=False, height=False)
	planner.configure(background='yellow')

	# ---- Request route ----
	def get_route():
		from_station = from_station_entry.get()
		to_station = to_station_entry.get()
		request = api_interface.reis_planner(from_station, to_station)

		# Clear listboxes before new request
		reisplanner_listbox.delete(0, END)

		for item in request:
			if item['optimaal'] == False:
				optimaal = 'Nee'
				colour_var = 'white'
			else:
				optimaal = 'Ja'
				colour_var = 'green'
			reisplanner_listbox.insert(END, '{0:<25} {1:<25} {2:<10} {3}'.format(item['vertrek_tijd'], item['aankomst_tijd'], item['aantal_overstappen'], optimaal))
			reisplanner_listbox.itemconfig(END, bg=colour_var, fg='black')

	# Input frame
	reisplanner_frame = Frame(planner, height=100, width=300, bd=2, relief=SUNKEN, bg='blue')
	reisplanner_frame.place(x=10, y=10)

	# From station label
	from_station_label = Label(reisplanner_frame, bg='blue', fg='yellow', text='Beginstation:')
	from_station_label.place(x=10, y=5)

	# From station input
	from_station_entry = Entry(reisplanner_frame, highlightbackground='blue')
	from_station_entry.place(x=130, y=5)

	# To station label
	to_station_label = Label(reisplanner_frame, bg='blue', fg='yellow', text='Eindstation:')
	to_station_label.place(x=10, y=35)

	# To station input
	to_station_entry = Entry(reisplanner_frame, highlightbackground='blue')
	to_station_entry.place(x=130, y=35)

	# Confirm button
	planner_submit = Button(reisplanner_frame, text='Bevestig', command=get_route, highlightbackground='blue')
	planner_submit.place(x=200, y=65)

	# Output frame
	output_frame = Frame(planner, height=220, width=550, bd=2, relief=SUNKEN)
	output_frame.place(x=10, y=130)	

	# Vertrektijd label
	vertrektijd_label = Label(output_frame, text='Vertrektijd')
	vertrektijd_label.place(x=10, y=7)

	# Aankomsttijd label
	aankomsttijd_label = Label(output_frame, text='Aankomsttijd')
	aankomsttijd_label.place(x=190, y=7)

	# Aantal overstappen
	overstappen_label = Label(output_frame, text='Overstappen')
	overstappen_label.place(x=340, y=7)

	# Optimale route
	optimaal_label = Label(output_frame, text='Optimaal?')
	optimaal_label.place(x=430, y=7)

	# Scrollbar for output
	reisplanner_scrollbar = Scrollbar(output_frame)
	reisplanner_scrollbar.place(x=525, y=25, height=173)

	# Reisplanner listbox
	reisplanner_listbox = Listbox(output_frame, yscrollcommand = reisplanner_scrollbar.set, width=73)
	reisplanner_listbox.place(x=10, y=25)

# ----- ANALYTICS WINDOW -----
def analytics():
	def reload_json():
		global json_data
		json_file = open("config.json", 'r')
		json_data = json.load(json_file)
		json_file.close()

		last_query_time_text['text'] = json_data['last_query_time']
		last_query_text['text'] = json_data['last_query']
		last_query_requests['text'] = json_data['requests']

	analytics = Toplevel()
	analytics.title('Applicatie Statistieken')
	analytics.geometry('800x200')
	analytics.resizable(width=False, height=False)
	analytics.configure(bg='yellow')

	#default_font = font.Font(family='Monaco', size=12)
	#analytics.option_add('*Font', default_font)

	statistieken_label = Label(analytics, text='Applicatie statistieken', fg='blue', bg='yellow')
	statistieken_label.place(x=10, y=5)

	# Main window
	stats_frame = Frame(analytics, height=160, width=777, bd=2, relief=SUNKEN)
	stats_frame.place(x=10, y=30)

	# tijd van laatste aanroep naar API
	last_query_time_label = Label(stats_frame, text='Gemaakt op: ')
	last_query_time_label.place(x=10, y=50)

	last_query_time_text = Label(stats_frame, text='')
	last_query_time_text.place(x=155, y=50)

	# laatste aanroep naar API
	last_query_label = Label(stats_frame, text='Laatste query: ')
	last_query_label.place(x=10, y=20)

	last_query_text = Label(stats_frame, text='')
	last_query_text.place(x=155, y=20)

	#aantal queries
	last_query_requests = Label (stats_frame, text="Aanvragen:")
	last_query_requests.place(x=10, y=80)

	last_query_requests = Label(stats_frame, text='')
	last_query_requests.place(x=155, y=80)

	reload_button = Button(stats_frame, text='Herlaad', command=reload_json)
	reload_button.place(x=400, y=100)

	reload_json()

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

button2 = Button(master=root, text='Reisplanner', command=reisplanner)
button2.pack(pady=13)

label = Label(master=root, text='Geef statistieken weer',
                 font=("Courier", 20),
                 width=200,
                 height=0,
                 background = 'yellow',
                 foreground = 'blue')
label.pack()

button3 = Button(master=root, text='Statistieken', command=analytics)
button3.pack(pady=15)

label.pack()
photo = "src/img/treinstation.gif"
image = PhotoImage(file=photo)
peace = Label(master=root,
              image=image,
              height=360)
peace.pack()

root.mainloop()

