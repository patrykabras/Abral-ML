from tkinter import ttk
from tkinter import filedialog
from tkinter import *
import os


class ModelsListGui:

    def create_models_list_frame(self, root):
        models_list_info_frame = Frame(root)
        model_list_label = Label(models_list_info_frame, {
            "width": 18,
            "padx": 2,
            "anchor": W,
            "text": "Models list",
            "font": 10
        })
        model_list_label.grid({
            "row": 0,
            "column": 0,
            "padx": 2,
            "pady": 8
        })

        self.__listbox_with_scrollbar(models_list_info_frame)

        choose_models_path = Button(models_list_info_frame, {
            "text": "Choose models directory",
            "width": 30,
            "bd": 3,
            "command": self.browse_button
        })
        choose_models_path.grid({
            "row": 2,
            "column": 0,
            "padx": 2,
            "pady": 8
        })
        currently_selected_label = Label(models_list_info_frame, {
            "width": 30,
            "padx": 10,
            # "bg": self.colors.get("myblue"),
            "text": "Currently selected:"
        })
        currently_selected_label.grid({
            "row": 3,
            "column": 0,
            "padx": 10,
            "pady": 4
        })
        self.currently_selected_entry = Entry(models_list_info_frame, {
            "bd": 2,
            "width": 35,
            "state": DISABLED
        })
        self.currently_selected_entry.grid({
            "row": 4,
            "column": 0,
            "padx": 10,
            "pady": 4
        })
        return models_list_info_frame

    def __listbox_with_scrollbar(self, tab):
        frameTemp = Frame(tab, {
            "height": 50,
            "width": 111,
        })
        self.listBox1 = Listbox(frameTemp, {
            "width": 40,
            "height": 22,
        })
        frameTemp.grid(row=1, column=0, sticky=W, padx=2, pady=2)
        self.listBox1.grid(row=0, column=0, sticky=NW, padx=2, pady=2)
        self.listBox1.bind('<<ListboxSelect>>', self.currently_selected)
        scrollb = Scrollbar(frameTemp, command=self.listBox1.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        self.listBox1['yscrollcommand'] = scrollb.set

    def currently_selected(self, evt):
        self.currently_selected_entry.configure(state=NORMAL)
        self.selected = self.listBox1.get(self.listBox1.curselection())
        self.currently_selected_entry.delete(0, END)
        self.currently_selected_entry.insert(0, self.selected)
        self.currently_selected_entry.configure(state=DISABLED)

    def browse_button(self):
        absPath = os.path.abspath(os.getcwd())
        self.dirpath = filedialog.askdirectory(initialdir=absPath, title="Please select a directory")
        entries = os.listdir(r'{}'.format(self.dirpath))
        self.listBox1.delete(0, END)
        for entry in entries:
            if entry.split(".")[1] == "sav":
                self.listBox1.insert(END, entry)
