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
        row1 = tk.Frame(self)
        row2 = tk.Frame(self)
        button1 = tk.Button(row1, text="Enter", command=lambda: cont.show_frame(EnterPage), font=LABEL_FONT)
        button1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        button2 = tk.Button(row1, text="Export", command=lambda: cont.show_frame(ExportPage), font=LABEL_FONT)
        button2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        button3 = tk.Button(row2, text="List", command=lambda: cont.show_frame(ListPage), font=LABEL_FONT)
        button3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        button4 = tk.Button(row2, text="Sum", command=lambda: cont.show_frame(SumPage), font=LABEL_FONT)
        button4.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        row1.pack(fill=tk.BOTH, expand=True)
        row2.pack(fill=tk.BOTH, expand=True)


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
        label1 = tk.Label(self, text="Calculate Sum: ", font=TITLE_FONT)
        label1.pack()
        label2 = tk.Label(self, text="Return total sum if blank", font=LABEL_FONT)
        label2.pack()
        entries = self.make_form()
        enter_button = tk.Button(self, text="Enter", command=lambda: self.fetch_sum(entries))
        enter_button.pack(side=tk.LEFT, padx=5, pady=5)
        back_button = tk.Button(self, text="Back", command=lambda: cont.show_frame(HomePage))
        back_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.result_message = tk.Label(self, text="", font=LABEL_FONT)
        self.result_message.pack()

    def make_form(self):
        ent1 = entry_maker(self, "Category: ")
        ent2 = entry_maker(self, "Date: ")
        return [ent1, ent2]

    def fetch_sum(self, entries):
        category = entries[0].get()
        clear_entry(entries[0])
        date = entries[1].get()
        clear_entry(entries[1])
        result = calculate_total(category, date)
        if result:
            update_label(self.result_message, "Total is: $" + str(result), "green")
        else:
            update_label(self.result_message, "Not found or input error", "red")


connect_db()
app = ExpenseTracker()
app.mainloop()
