import tkinter as tk
import requests
import threading
from PIL import ImageTk, Image

URL="http://127.0.0.1:8000/WIMPSite/api/test/add_test/"


def post(json):
    request = requests.post(URL, json=json)

    print(request.text)


def from_rgb(rgb):
    return "#%02x%02x%02x" % rgb


class Chemical_Test:
    def __init__(self, parent, row, callback):
        self.r = 0
        self.g = 0
        self.b = 0

        self.test_label = tk.Label(parent, name=str(row), width="25", text="Test %d" % (int(row / 3)))
        self.test_label.bind("<Button-1>", callback)
        self.test_label.grid(columnspan=2, column=0, row=row)

        self.text_label = tk.Label(parent, text="Text", width=10)
        self.text_label.grid(sticky=tk.W, column=0, row=row + 1)
        self.text_entry = tk.Entry(parent, width=15)
        self.text_entry.grid(column=1, row=row + 1)

        self.value_label = tk.Label(parent, text="Value", width=10)
        self.value_label.grid(sticky=tk.W, column=0, row=row + 2)
        self.value_entry = tk.Entry(parent, width=15)
        self.value_entry.grid(column=1, row=row + 2)

    def set_color(self, color):
        self.test_label.config(bg=from_rgb(color))

        self.r = color[0]
        self.g = color[1]
        self.b = color[2]

class WIMP_GUI:
    def __init__(self, window):
        self.current_test = 0
        self.window = window
        path = "test.jpg"

        self.image = Image.open(path)

        size = 500, 500
        self.image.thumbnail(size, Image.ANTIALIAS)

        self.img = ImageTk.PhotoImage(self.image)

        img_view = tk.Label(self.window, name="img", image=self.img, anchor=tk.E, justify=tk.RIGHT, background="red")
        img_view.anchor(tk.E)
        img_view.bind("<Button-1>", self.color_callback)
        img_view.grid(column=2, rowspan=25)

        self.test_info_label = tk.Label(self.window, text="Test Info", bg="white", width=25)
        self.test_info_label.grid(column=0, columnspan=2, row=0)

        self.test_name_label = tk.Label(self.window, name="testname", text="Test Name", width=10)
        self.test_name_label.grid(column=0, row=1)
        self.test_name_entry = tk.Entry(self.window, width=15)
        self.test_name_entry.grid(column=1, row=1)

        self.test_unit_label = tk.Label(self.window, name="unit", text="Unit", width=10)
        self.test_unit_label.grid(column=0, row=2)
        self.test_unit_entry = tk.Entry(self.window, width=15)
        self.test_unit_entry.grid(column=1, row=2)

        self.test_id_label = tk.Label(self.window, name="test_id", text="Strip ID", width=10)
        self.test_id_label.grid(column=0, row=3)
        self.test_id_entry = tk.Entry(self.window, width=15)
        self.test_id_entry.grid(column=1, row=3)

        self.output_view = tk.Label(self.window, text="Color Select", bg="white", width=25)
        self.output_view.grid(column=0, columnspan=2, row=4)

        self.test_chart = []

        for i in range(5, 19, 3):
            test = Chemical_Test(self.window, i, self.test_select_callback)
            self.test_chart.append(test)

        self.submit = tk.Label(self.window, text="Submit", bg="green", width=25)
        self.submit.bind("<Button-1>", self.submit_callback)
        self.submit.grid(column=0, columnspan=2, row=20)

    def color_callback(self, event):
        color = self.image.load()[event.x, event.y]
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

        post_thread = threading.Thread(target=post, args=(json, ))

        post_thread.start()


if __name__ == "__main__":
    window = tk.Tk()
    window.title("WIMP Color Input")
    window.configure(background='grey')

    gui = WIMP_GUI(window)
    window.mainloop()
