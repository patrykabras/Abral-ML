from tkinter import ttk
from tkinter import filedialog
from tkinter import *


class OutputGui:

    def create_output_frame(self, root):
        output_frame = Frame(root)
        output_label = Label(output_frame, {
            "width": 60,
            "padx": 10,
            "anchor": W,
            "text": "Output",
            "font": 10
        })
        output_label.grid({
            "row": 0,
            "column": 0,
            "padx": 4,
            "pady": 4
        })
        self.__textbox_with_scrollbar(output_frame)
        return output_frame

    def __textbox_with_scrollbar(self, tab):
        frameTemp = Frame(tab, {
            "height": 40,
            "width": 90,
        })
        frameTemp.grid(row=1, column=0, sticky=W, padx=2, pady=2)
        self.text = Text(frameTemp, {
            "height": 21,
            "width": 95,
        })
        self.text.grid(row=0, column=0, sticky=NW, padx=2, pady=2)
        scrollb = Scrollbar(frameTemp, command=self.text.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        self.text['yscrollcommand'] = scrollb.set
        self.text.config(state=DISABLED)
