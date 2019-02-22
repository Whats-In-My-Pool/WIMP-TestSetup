import tkinter as tk
from test_edit_view import TestEditView
from test_strip_select import TestStripSelect, TestStripEnter


class WIMPApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.winfo_toplevel().title("WIMP")
        self.strip_id = tk.IntVar(self)
        self.img_path = tk.StringVar(self)

        self.test_strip_select = TestStripSelect(window=container, controller=self)
        self.test_strip_select.grid(row=0, column=0, sticky="nsew")

        self.test_input = TestEditView(window=container, controller=self)
        self.test_input.grid(row=1, column=0, sticky="nsew")

        self.strip_input = TestStripEnter(window=container, controller=self)
        self.strip_input.grid(row=0, column=0, sticky="nsew")

        self.test_strip_select.tkraise()


if __name__ == "__main__":
    window = WIMPApp()
    window.mainloop()
