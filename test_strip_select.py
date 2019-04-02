import tkinter as tk
from tkinter import filedialog
from wimp_api import get_test_strips, post_test_strip


class TestStripSelect(tk.Frame):
    def __init__(self, window, controller):
        self.window = window
        self.controller = controller

        tk.Frame.__init__(self, window)

        tk.Label(self, text="Test Strip").grid(row=0, column=0)

        strips = get_test_strips()

        self.choices = {}

        for strip in strips:
            self.choices[strip["fields"]["name"]] = strip["pk"]

        self.choices["Add new strip"] = -1

        self.menu_sel = tk.StringVar(window)

        self.menu_sel.set(next(iter(self.choices.keys())))

        self.inflate_menu()

        b = tk.Button(self, text="Select", command=self.button_callback)
        b.grid(row=0, column=3)

        b = tk.Button(self, text="Select Color Char", command=self.select_chart_callback)
        b.grid(row=0, column=4)

    def inflate_menu(self):
        self.popupMenu = tk.OptionMenu(self, self.menu_sel, *self.choices)
        self.popupMenu.config(width=25)
        self.popupMenu.grid(row=0, column=1)


    def select_chart_callback(self):
        self.controller.img_path.set(tk.filedialog.askopenfilename(initialdir=".", title="Select file",
                                             filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*"))))

    def button_callback(self):
        id = self.choices[self.menu_sel.get()]

        if id == -1:
            self.controller.strip_input.tkraise()
        else:
            self.controller.strip_id.set(id)
            self.controller.test_input.tkraise()


class TestStripEnter(tk.Frame):
    def __init__(self, window, controller):
        self.window = window
        self.controller = controller
        tk.Frame.__init__(self, window)

        tk.Label(self, text="New Strip Name").grid(row=0, column=0)

        self.test_name_entry = tk.Entry(self)
        self.test_name_entry.grid(column=2, row=0)

        self.b = tk.Button(self, text="Submit", command=self.button_callback)
        self.b.grid(row=0, column=3)

        self.c = tk.Button(self, text="Cancel", command=self.back_callback)
        self.c.grid(row=0, column=4)

    def button_callback(self):
        id = post_test_strip(self.test_name_entry.get())

        self.controller.strip_id.set(id)
        self.controller.test_strip_select.tkraise()
        self.controller.test_strip_select.choices[self.test_name_entry.get()] = id

        self.controller.test_strip_select.menu_sel = self.test_name_entry.get()
        self.controller.test_strip_select.inflate_menu()


    def back_callback(self):
        print("Test")
        self.controller.test_strip_select.tkraise()
