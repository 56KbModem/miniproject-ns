from tkinter import *
from tkinter import Tk, Label, PhotoImage

root = Tk()
root.configure(bg='white')

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

button1 = Button(master=root, text='Actuele vertrektijden')
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
photo = "treinstation.gif"
image = PhotoImage(file=photo)
peace = Label(master=root,
              image=image,
              height=360)
peace.pack()

root.mainloop()

