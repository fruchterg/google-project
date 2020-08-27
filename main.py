from online import *
from offline import ignorecharacter
from tkinter import *

win = Tk()
win.title("Python GUI App")


def print_autocomplete(best_complete):
    if best_complete == list():
        list_.insert(END, "NO SUGESTIONS :(")
        e1.delete(0, END)
    for obj in best_complete:
        list_.insert(END, obj.get_completed_sentence() + "(" + obj.get_source_text() + " " + str(obj.get_offset()) + ")"
                     + str(obj.get_score()) + "\n")


def start_app(string):
    if string and string[-1] != '#':
        return print_autocomplete(autocompleteData(ignorecharacter(string)))
    e1.delete(0, END)


def click():
    list_.delete(0, END)
    list_.insert(END, start_app(e1.get()))


Label(win, text='press your search').grid(row=0)
e1 = Entry(win, width=80)
e1.grid(row=0, column=0)
button = Button(win, text='Search', width=10, height=1, command=click)
button.grid(row=0, column=1)
list_ = Listbox(win, width=80)
list_.grid(row=1, column=0)
win.mainloop()

db_file.close()
