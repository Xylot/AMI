from tkinter import *
master = Tk()

w = Canvas(master, width=1000, height=500)

for x in range(0,9):
	w.create_rectangle(x * 100 + 10, 10, x * 100 + 100, 110, fill="black")
	w.create_text(((x * 100) + 55, 55), text="1", fill="white")


#w.create_rectangle(0, 0, 100, 100, fill="black", outline = 'black')
#w.create_rectangle(110, 0, 210, 100, fill="blue", outline = 'blue')
#w.create_rectangle(50, 50, 100, 100, fill="red", outline = 'blue') 
w.pack()
master.mainloop()