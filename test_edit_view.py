import threading
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from wimp_api import post_chemical_test


def from_rgb(rgb):
    return "#%02x%02x%02x" % rgb


class Chemical_Test:
    def __init__(self, parent, row, callback):
        self.r = 0
        self.g = 0
        self.b = 0

        self.test_label = tk.Label(parent, name=str(row), width="25", text="Test %d" % (int(row / 3)))
        self.test_label.bind("<Button-1>", callback)
        self.test_label.grid(columnspan=2, column=0, row=row, sticky="nsew")

        self.text_label = tk.Label(parent, text="Text", width=10)
        self.text_label.grid(sticky=tk.W, column=0, row=row + 1)
        self.text_entry = tk.Entry(parent, width=15)
        self.text_entry.grid(column=1, row=row + 1, sticky="nsew")

        self.value_label = tk.Label(parent, text="Value", width=10)
        self.value_label.grid(sticky=tk.W, column=0, row=row + 2)
        self.value_entry = tk.Entry(parent, width=15)
        self.value_entry.grid(column=1, row=row + 2, sticky="nsew")

    def clear(self):
        self.text_entry.delete(0, 'end')
        self.value_entry.delete(0, 'end')

    def set_color(self, color):
        self.test_label.config(bg=from_rgb(color))

        self.r = color[0]
        self.g = color[1]
        self.b = color[2]


class TestEditView(tk.Frame):
    def __init__(self, window, controller):
        tk.Frame.__init__(self, window)

        self.current_test = 0
        self.window = window
        self.controller = controller

        image = ImageTk.PhotoImage(Image.new('RGB', (500, 500), (255, 255, 255)))

        self.img_view = tk.Label(self, name="img", image=image)
        self.img_view.anchor(tk.E)
        self.img_view.bind("<Button-1>", self.color_callback)
        self.img_view.grid(column=2, rowspan=25)

        self.test_info_label = tk.Label(self, text="Test Info", bg="white", width=25)
        self.test_info_label.grid(column=0, columnspan=2, row=0, sticky="nsew")

        self.test_name_label = tk.Label(self, name="testname", text="Test Name", width=10)
        self.test_name_label.grid(column=0, row=1)
        self.test_name_entry = tk.Entry(self, width=15)
        self.test_name_entry.grid(column=1, row=1, sticky="nsew")

        self.test_unit_label = tk.Label(self, name="unit", text="Unit", width=10)
        self.test_unit_label.grid(column=0, row=2)
        self.test_unit_entry = tk.Entry(self, width=15)
        self.test_unit_entry.grid(column=1, row=2, sticky="nsew")

        self.test_id_label = tk.Label(self, name="test_id", text="Strip ID", width=10)
        self.test_id_label.grid(column=0, row=3)
        self.test_id_entry = tk.Entry(self, width=15, textvariable=window)
        self.test_id_entry.grid(column=1, row=3, sticky="nsew")

        self.output_view = tk.Label(self, text="Color Select", bg="white", width=25)
        self.output_view.grid(column=0, columnspan=2, row=4, sticky="nsew")

        self.test_chart = []

        for i in range(5, 19, 3):
            test = Chemical_Test(self, i, self.test_select_callback)
            self.test_chart.append(test)

        self.submit = tk.Button(self, text="Submit", bg="green", width=25)
        self.submit.bind("<Button-1>", self.submit_callback)
        self.submit.grid(column=0, columnspan=2, row=20)

        controller.strip_id.trace("w", self.strip_changed_callback)
        self.controller.img_path.trace("w", self.img_change_callback)

    def blank(self):
        self.test_name_entry.delete(0, 'end')
        self.test_unit_entry.delete(0, 'end')
        self.test_id_entry.delete(0, 'end')

        for test in self.test_chart:
            test.clear()

    def color_callback(self, event):
        img = self.image.load()

        r = 0
        g = 0
        b = 0
        count = 0
        size = 2
        for x in range(event.x-size, event.x+size):
            for y in range(event.y-size, event.y+size):
                r += img[x, y][0]
                g += img[x, y][1]
                b += img[x, y][2]
                count += 1

        color = (int(r/count), int(g/count), int(b/count))

        print("clicked at", event.x, event.y)
        print("color: {}".format(color))
        self.output_view.config(text="color: {}".format(color))
        self.output_view.config(bg=from_rgb(color))

        self.test_chart[self.current_test].set_color(color)

    def test_select_callback(self, event):
        self.test_chart[self.current_test].test_label.config(relief=tk.FLAT)
        self.current_test = int(int(event.widget._name)/3) - 1

        self.test_chart[self.current_test].test_label.config(relief=tk.RAISED)

    def submit_callback(self, event):
        json = {}

        json["strip_id"] = self.test_id_entry.get()
        json["unit"] = self.test_unit_entry.get()
        json["strip_name"] = self.test_name_entry.get()

        colors = []
        for test in self.test_chart:
            color = {}

            color["unit_value"] = test.value_entry.get()
            color["text"] = test.text_entry.get()
            color["r"] = test.r
            color["g"] = test.g
            color["b"] = test.b

            colors.append(color)

        json["colors"] = colors

        post_thread = threading.Thread(target=post_chemical_test, args=(json,))

        post_thread.start()

        self.blank()

    def img_change_callback(self, *args):
        path = self.controller.img_path.get()

        if path != "":
            self.image = Image.open(path)

            size = 500, 500
            self.image.thumbnail(size, Image.ANTIALIAS)

            self.img = ImageTk.PhotoImage(self.image)

            self.img_view.config(image=self.img, width=500)

    def strip_changed_callback(self, *args):
        id = self.controller.strip_id.get()

        self.test_id_entry.insert(0, id)




