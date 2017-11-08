import json
from tkinter import *
from tkinter import font

def reload_json():
    global json_data
    json_file = open("config.json", 'r')
    json_data = json.load(json_file)
    json_file.close()

    last_query_time_text['text'] = json_data['last_query_time']
    last_query_text['text'] = json_data['last_query']
    last_query_requests['text'] = json_data['requests']

root = Tk()
root.title('Statistieken')
root.geometry('1100x400')
root.resizable(width=False, height=False)
root.configure(bg='white')
default_font = font.Font(family='Monaco', size=12)
root.option_add('*Font', default_font)

statistieken_label = Label(root, text='Applicatie statistieken')
statistieken_label.place(x=10, y=10)

# Main window
stats_frame = Frame(root, height=300, width=1000, bd=2, relief=SUNKEN)
stats_frame.place(x=10, y=50)


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
root.mainloop()