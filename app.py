import tkinter as tk
import os
from tracker import *
from sqlite3 import OperationalError

# global vars
TITLE_FONT = ("Verdana", 12)
LABEL_FONT = ("Verdana", 8)


# global helper funcs
def entry_maker(cont, label):
    row = tk.Frame(cont)
    lab = tk.Label(row, width=15, text=label, anchor='w')
    ent = tk.Entry(row)
    row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
    lab.pack(side=tk.LEFT)
    ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
    return ent


def clear_entry(ent):
    ent.delete(0, 'end')
    ent.insert(0, '')


def update_label(label, message, color):
    label.configure(text=message, fg=color)
    label.update()


# classes
class ExpenseTracker(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for FRAME in (HomePage, EnterPage, ListPage, SumPage, ExportPage):
            frame = FRAME(container, self)
            frame.grid(row=0, column=0, sticky='nsew')
            self.frames[FRAME] = frame
        self.show_frame(HomePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class HomePage(tk.Frame):
    def __init__(self, parent, cont):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Expense Tracker", font=TITLE_FONT)
        label.pack()
        button1 = tk.Button(self, text="Enter", command=lambda: cont.show_frame(EnterPage))
        button1.pack()
        button2 = tk.Button(self, text="List", command=lambda: cont.show_frame(ListPage))
        button2.pack()
        button3 = tk.Button(self, text="Sum", command=lambda: cont.show_frame(SumPage))
        button3.pack()
        button4 = tk.Button(self, text="Export", command=lambda: cont.show_frame(ExportPage))
        button4.pack()


class EnterPage(tk.Frame):
    def __init__(self, parent, cont):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Enter an Expense", font=TITLE_FONT)
        label.pack()

        fields = 'Description', 'Category', 'Price'
        entries = self.make_form(fields)

        enter_button = tk.Button(self, text="Enter", command=lambda: self.fetch_entries(entries))
        enter_button.pack(side=tk.LEFT, padx=5, pady=5)
        back_button = tk.Button(self, text="Back", command=lambda: cont.show_frame(HomePage))
        back_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.warning_message = tk.Label(self, text="", font=LABEL_FONT)
        self.warning_message.pack()

    def make_form(self, fields):
        entries = []
        for field in fields:
            ent = entry_maker(self, field)
            entries.append(ent)
        return entries

    # fetch from entry fields, create entry, clear fields
    def fetch_entries(self, entries):
        inp = []
        empty_field = False
        for entry in entries:
            text = entry.get()
            if not text:
                empty_field = True
            inp.append(text)
            clear_entry(entry)
        if empty_field:
            # when form left empty
            update_label(self.warning_message, "Fill out everything", "red")
        else:
            try:
                # successful entry
                create_entry(inp[0], inp[1], inp[2])
                update_label(self.warning_message, "Success", "green")
            except OperationalError:
                # when non-numeric chars is inputted in price field
                update_label(self.warning_message, "Price should be numeric", "red")


class ListPage(tk.Frame):
    def __init__(self, parent, cont):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="List Expenses by: ", font=TITLE_FONT)
        label.pack()
        button1 = tk.Button(self, text="Back", command=lambda: cont.show_frame(HomePage))
        button1.pack()


class ExportPage(tk.Frame):
    def __init__(self, parent, cont):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Export as Excel", font=TITLE_FONT)
        label.pack()
        entry = self.make_form()
        enter_button = tk.Button(self, text="Enter", command=lambda: self.fetch_file(entry))
        enter_button.pack(side=tk.LEFT, padx=5, pady=5)
        back_button = tk.Button(self, text="Back", command=lambda: cont.show_frame(HomePage))
        back_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.warning_message = tk.Label(self, text="", font=LABEL_FONT)
        self.warning_message.pack()

    def make_form(self):
        ent = entry_maker(self, "Enter Filename: ")
        return ent

    def fetch_file(self, entry):
        text = entry.get()
        clear_entry(entry)
        if not text:
            text = "default"
        filename = text + ".xls"
        data = list_all()
        # if file already exists, override
        # else make new file
        if os.path.exists(filename):
            # warn if file is currently being used
            try:
                os.remove(filename)
            except PermissionError:
                update_label(self.warning_message, "File exists & being used", "red")
        export_entries(filename, data)
        update_label(self.warning_message, "Success", "green")


class SumPage(tk.Frame):
    def __init__(self, parent, cont):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Total Expenses by: ", font=TITLE_FONT)
        label.pack()
        button1 = tk.Button(self, text="Back", command=lambda: cont.show_frame(HomePage))
        button1.pack()


connect_db()
app = ExpenseTracker()
app.mainloop()
