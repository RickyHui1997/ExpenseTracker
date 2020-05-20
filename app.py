import tkinter as tk


TITLE_FONT = ("Verdana", 12)
LABEL_FONT = ("Verdana", 8)

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


def dummy_func():
    print("works")


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

        self.fields = 'Description', 'Category', 'Price'
        entries = self.make_form()

        enter_button = tk.Button(self, text="Enter", command=lambda: self.fetch_entries(entries))
        enter_button.pack(side=tk.LEFT, padx=5, pady=5)
        back_button = tk.Button(self, text="Back", command=lambda: cont.show_frame(HomePage))
        back_button.pack(side=tk.LEFT, padx=5, pady=5)

    def make_form(self):
        entries = []
        for field in self.fields:
            row = tk.Frame(self)
            lab = tk.Label(row, width=15, text=field, anchor='w')
            ent = tk.Entry(row)
            row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
            lab.pack(side=tk.LEFT)
            ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
            entries.append((field, ent))
        return entries

    def fetch_entries(self, entries):
        for entry in entries:
            field = entry[0]
            text = entry[1].get()
            entry[1].delete(0, 'end')
            entry[1].insert(0, '')
            print('%s: "%s"' % (field, text))




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
        button1 = tk.Button(self, text="Back", command=lambda: cont.show_frame(HomePage))
        button1.pack()


class SumPage(tk.Frame):
    def __init__(self, parent, cont):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Total Expenses by: ", font=TITLE_FONT)
        label.pack()
        button1 = tk.Button(self, text="Back", command=lambda: cont.show_frame(HomePage))
        button1.pack()


app = ExpenseTracker()
app.mainloop()
