from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
import gui_ml.OutputGui as Output_gui

from ml.MachineLearning import MachineLearning
from data_db_connector.DBConnector import DBConnector
from db_tables.Completed_Table import Completed_Table

import os


class GeneralInfoGui:

    def __init__(self, output_gui: Output_gui):
        self.output_gui = output_gui

    def create_general_frame(self, root):
        # general_info_frame Start
        general_info_frame = Frame(root)

        h1 = Label(general_info_frame, {
            "padx": 5,
            # "bg": self.colors.get("myblue"),
            "text": "Models config",
            "font": 10
        })
        h1.grid({
            "row": 0,
            "column": 0,
            "padx": 5,
            "pady": 4
        })

        select_algorithm_label = Label(general_info_frame, {
            "width": 20,
            "padx": 5,
            "anchor": W,
            "text": "Select algorithm:"
        })
        select_algorithm_label.grid({
            "row": 1,
            "column": 0,
            "padx": 5,
            "pady": 4
        })

        self.radio_button_var = IntVar()
        radio1 = Radiobutton(general_info_frame, {
            "text": "KNeighborsClassifier",
            "variable": self.radio_button_var,
            "value": 1,
            "command": self.radiobutton_sellect
        })
        radio1.grid({
            "row": 2,
            "column": 0,
            "padx": 5,
            "pady": 4
        })
        radio2 = Radiobutton(general_info_frame, {
            "text": "KNeighborsRegressor",
            "variable": self.radio_button_var,
            "value": 2,
            "command": self.radiobutton_sellect
        })
        radio2.grid({
            "row": 2,
            "column": 1,
            "padx": 5,
            "pady": 4
        })

        model_file_name_label = Label(general_info_frame, {
            "width": 20,
            "padx": 5,
            "anchor": W,
            "text": "Model file name:"
        })
        model_file_name_label.grid({
            "row": 3,
            "column": 0,
            "padx": 5,
            "pady": 4
        })

        self.model_file_name_entry = Entry(general_info_frame, {
            "width": 50,
            "bd": 2
        })
        self.model_file_name_entry.grid({
            "row": 3,
            "column": 1,
            "padx": 5,
            "pady": 4
        })

        model_save_path_label = Label(general_info_frame, {
            "width": 20,
            "padx": 5,
            "anchor": W,
            "text": "Model save path:"
        })
        model_save_path_label.grid({
            "row": 4,
            "column": 0,
            "padx": 5,
            "pady": 4
        })

        self.model_save_path_entry = Entry(general_info_frame, {
            "width": 50,
            "bd": 2,
            "state": DISABLED
        })
        self.model_save_path_entry.grid({
            "row": 4,
            "column": 1,
            "padx": 5,
            "pady": 4
        })

        browse_model_save_btn = Button(general_info_frame, {
            "text": "Browse",
            "width": 20,
            "bd": 3,
            "command": self.browse_button
        })
        browse_model_save_btn.grid({
            "row": 5,
            "column": 0,
            "padx": 5,
            "pady": 4
        })
        save_model_btn = Button(general_info_frame, {
            "text": "Save model",
            "width": 20,
            "bd": 3,
            "command": self.save_model
        })
        save_model_btn.grid({
            "row": 5,
            "column": 1,
            "padx": 2,
            "pady": 1
        })

        test_size_label = Label(general_info_frame, {
            "width": 20,
            "padx": 5,
            "anchor": W,
            "text": "Test size: "
        })
        test_size_label.grid({
            "row": 3,
            "column": 2,
            "padx": 5,
            "pady": 4
        })

        self.test_size_entry = Entry(general_info_frame, {
            "bd": 2
        })
        self.test_size_entry.grid({
            "row": 3,
            "column": 3,
            "padx": 5,
            "pady": 4
        })
        self.test_size_entry.insert(INSERT, "0.2")

        amount_of_data_label = Label(general_info_frame, {
            "width": 20,
            "padx": 5,
            "anchor": W,
            "text": "Amount of data: "
        })
        amount_of_data_label.grid({
            "row": 4,
            "column": 2,
            "padx": 5,
            "pady": 4
        })

        self.amount_of_data_entry = Entry(general_info_frame, {
            "bd": 2
        })
        self.amount_of_data_entry.grid({
            "row": 4,
            "column": 3,
            "padx": 5,
            "pady": 4
        })

        start_learn_btn = Button(general_info_frame, {
            "text": "Start learning",
            "width": 20,
            "bd": 3,
            "command": self.start_learn
        })
        start_learn_btn.grid({
            "row": 5,
            "column": 2,
            "columnspan": 2,
            "padx": 2,
            "pady": 1
        })
        return general_info_frame

    def radiobutton_sellect(self):
        selection = "You selected the option " + str(self.radio_button_var.get())
        print(selection)

    def browse_button(self):
        absPath = os.path.abspath(os.getcwd())
        self.dirpath = filedialog.askdirectory(initialdir=absPath, title="Please select a directory")
        print(self.dirpath)
        self.model_save_path_entry.configure(state=NORMAL)
        self.model_save_path_entry.delete(0, END)
        self.model_save_path_entry.insert(END, self.dirpath)

    def start_learn(self):
        # model, acc, self_acc, prediction, x_test, y_test, epsilon
        self.output_gui.text.config(state=NORMAL)
        self.output_gui.text.delete('1.0', END)

        amount_of_data = 0
        if int(self.amount_of_data_entry.get()) > 0:
            amount_of_data = int(self.amount_of_data_entry.get())

        mltemp = MachineLearning()
        dbc = DBConnector()
        cnx_pool = dbc.create_connection(32)

        completed_table = Completed_Table(cnx_pool)
        records = completed_table.collect_data(0, amount_of_data)
        model, acc, self_acc, prediction, x_test, y_test, epsilon = mltemp.k_neighbors(records, float(
            self.test_size_entry.get()))
        self.current_model = model

        self.output_gui.text.insert(INSERT, "Self made accuracy calculators: \n")
        self.output_gui.text.insert(INSERT, "\n")
        self.output_gui.text.insert(INSERT, "Prediction is classified as correct when belongs to range: \n")
        self.output_gui.text.insert(INSERT, "from actual_value - {}h to actual_value + {}h \n".format(epsilon, epsilon))
        self.output_gui.text.insert(INSERT,
                                    "Classification accuracy = {} \n".format(self_acc))
        self.output_gui.text.insert(INSERT, "Sklearn.score(): {}\n".format(acc))

        self.output_gui.text.insert(INSERT, "\nPredictions: \n")
        self.output_gui.text.insert(INSERT, "\n")
        for x in range(len(prediction)):
            self.output_gui.text.insert(INSERT, "Predicted: {} Data: {} Actual: {} \n".format(prediction[x], x_test[x],
                                                                                              y_test[x]))
        self.output_gui.text.config(state=DISABLED)

    def save_model(self):
        filename = self.model_file_name_entry.get()
        dir_path = self.dirpath
        complete_path = dir_path + "/" + filename + ".sav"
        mltemp = MachineLearning()
        mltemp.save_model(self.current_model, complete_path)
        messagebox.showinfo("Success", "Model {} saved".format(filename))
