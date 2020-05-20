from tkinter import ttk
from tkinter import filedialog
from tkinter import *
from ml.MachineLearning import MachineLearning
from data_db_connector.DBConnector import DBConnector
from db_tables.Completed_Table import Completed_Table

import pickle
import math
from sklearn import linear_model, preprocessing
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import KNeighborsRegressor
import sklearn
import numpy


class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.colors = {
            "myblue": "#4eaef2",
            "mygreen": "#16db04",
            "myred": "#dd0202"
        }
        self.master.geometry("1200x800")
        self.master.title("Abral - Projekt - Tracking z wykorzystaniem uczenia maszynowego")
        # self.master.iconphoto(False, PhotoImage(file='gui_ml/abral-icon.png'))
        self.master.call('wm', 'iconphoto', self.master._w, PhotoImage(file='gui_ml/abral-icon.png'))
        self.pack()
        self.master.configure(bg='blue')
        self.createWidgets()

    def donothing(self):
        print("Do nothing")

    def create_style(self):
        self.style = ttk.Style()
        self.style.theme_create("MyStyle", parent="alt", settings={
            "TNotebook": {"configure": {
                "tabmargins": [2, 5, 2, 0],
                "background": "grey"
            }},
            "TNotebook.Tab": {
                "configure": {
                    "padding": [5, 5],
                    "margin": [5, 2],
                },
                "map": {
                    "background": [("selected", self.colors.get("mygreen"))],
                    "expand": [("selected", [1, 1, 1, 0])]
                }
            },
            "TFrame": {"configure": {
                "background": self.colors.get("myblue")
            }
            }
        })
        self.style.theme_use("MyStyle")

    def createWidgets(self):
        self.create_style()
        tabControl = ttk.Notebook(self, width=1200, height=800)

        self.tab1 = ttk.Frame(tabControl)
        tab2 = ttk.Frame(tabControl)

        tabControl.add(self.tab1, text='Predict from loaded model')
        tabControl.add(tab2, text='Tab 2')
        tabControl.pack({
            "side": LEFT,
            "fill": BOTH,
        })
        Label(tab2,
              text="Lets dive into the\
        world of computers").grid(column=0,
                                  row=0,
                                  padx=30,
                                  pady=30)

        self.__addMenu()
        # self.__textbox_with_scrollbar(self.tab1)
        # self.__allEntry(self.tab1)
        self.general_info()
        self.output_info()
        self.single_prediction_info()
        self.actions_menu_info()
        self.models_list_info()
        # self.__allListBox()

    def browse_button(self):
        # Allow user to select a directory and store it in global var
        # called folder_path
        filename = filedialog.askopenfilename(initialdir="/", title="Select A File", filetype=(("txt files", "*.txt"),
                                                                                               ("all files", "*.*")))
        self.folder_path.set(filename)
        print(filename)

    def general_info(self):
        # general_info_frame Start
        general_info_frame = Frame(self.tab1)
        general_info_frame.grid({
            "row": 0,
            "column": 0,
            "padx": 5,
            "pady": 20
        })

        self.folder_path = StringVar()
        lbl1 = Label(general_info_frame, textvariable=self.folder_path)
        lbl1.grid(row=0, column=1)
        button2 = Button(general_info_frame, text="Browse", command=self.browse_button)
        button2.grid(row=0, column=3)

        h1 = Label(general_info_frame, {
            "padx": 5,
            # "bg": self.colors.get("myblue"),
            "text": "General Info",
            "font": 10
        })
        h1.grid({
            "row": 0,
            "column": 0,
            "padx": 5,
            "pady": 4
        })

        label_names = ("Database host:", "Database name:", "User:", "Password:")
        for i in range(1, 5):
            l1 = Label(general_info_frame, {
                "width": 12,
                "padx": 5,
                "anchor": W,
                # "bg": self.colors.get("myblue"),
                "text": label_names[i - 1]
            })
            l1.grid({
                "row": i,
                "column": 0,
                "padx": 5,
                "pady": 4
            })

        self.db_host_entry = Entry(general_info_frame, {
            "bd": 2
        })
        self.db_host_entry.grid({
            "row": 1,
            "column": 1,
            "padx": 5,
            "pady": 4
        })
        db_name_entry = Entry(general_info_frame, {
            "bd": 2
        })
        db_name_entry.grid({
            "row": 2,
            "column": 1,
            "padx": 5,
            "pady": 4
        })
        db_user_entry = Entry(general_info_frame, {
            "bd": 2
        })
        db_user_entry.grid({
            "row": 3,
            "column": 1,
            "padx": 5,
            "pady": 4
        })
        db_password_entry = Entry(general_info_frame, {
            "bd": 2
        })
        db_password_entry.grid({
            "row": 4,
            "column": 1,
            "padx": 5,
            "pady": 4
        })

        test_connection_bttn = Button(general_info_frame, {
            "text": "Test connection",
            "width": 25,
            "bd": 3
        })
        test_connection_bttn.grid({
            "row": 5,
            "columnspan": 2,
            "column": 0,
            "padx": 5,
            "pady": 4
        })

        select_algorithm_label = Label(general_info_frame, {
            "width": 20,
            "padx": 5,
            "anchor": W,
            # "bg": self.colors.get("myblue"),
            "text": "Select algorithm:"
        })
        select_algorithm_label.grid({
            "row": 1,
            "column": 2,
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
            "column": 2,
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
            "column": 3,
            "padx": 5,
            "pady": 4
        })

        model_file_name_label = Label(general_info_frame, {
            "width": 20,
            "padx": 5,
            "anchor": W,
            # "bg": self.colors.get("myblue"),
            "text": "Model file name:"
        })
        model_file_name_label.grid({
            "row": 3,
            "column": 2,
            "padx": 5,
            "pady": 4
        })

        model_file_name_entry = Entry(general_info_frame, {
            "bd": 2
        })
        model_file_name_entry.grid({
            "row": 3,
            "column": 3,
            "padx": 5,
            "pady": 4
        })

        model_save_path_label = Label(general_info_frame, {
            "width": 20,
            "padx": 5,
            "anchor": W,
            # "bg": self.colors.get("myblue"),
            "text": "Model save path:"
        })
        model_save_path_label.grid({
            "row": 4,
            "column": 2,
            "padx": 5,
            "pady": 4
        })

        model_save_path_entry = Entry(general_info_frame, {
            "bd": 2
        })
        model_save_path_entry.grid({
            "row": 4,
            "column": 3,
            "padx": 5,
            "pady": 4
        })

        browse_algorithm_btn = Button(general_info_frame, {
            "text": "Browse",
            "width": 20,
            "bd": 3
        })
        browse_algorithm_btn.grid({
            "row": 5,
            "column": 2,
            "padx": 5,
            "pady": 4
        })
        check_path_algorithm_btn = Button(general_info_frame, {
            "text": "Check path",
            "width": 20,
            "bd": 3
        })
        check_path_algorithm_btn.grid({
            "row": 5,
            "column": 3,
            "padx": 5,
            "pady": 4
        })

        rpt_file_path_label = Label(general_info_frame, {
            "width": 20,
            "padx": 5,
            "anchor": W,
            # "bg": self.colors.get("myblue"),
            "text": "RPT file path:"
        })
        rpt_file_path_label.grid({
            "row": 2,
            "column": 4,
            "padx": 5,
            "pady": 4
        })

        rpt_file_path_entry = Entry(general_info_frame, {
            "bd": 2
        })
        rpt_file_path_entry.grid({
            "row": 2,
            "column": 5,
            "padx": 5,
            "pady": 4
        })

        rpt_file_path_browse_btn = Button(general_info_frame, {
            "text": "Check path",
            "width": 20,
            "bd": 3
        })
        rpt_file_path_browse_btn.grid({
            "row": 3,
            "column": 4,
            "padx": 5,
            "pady": 4
        })

        rpt_file_path_check_path_btn = Button(general_info_frame, {
            "text": "Check path",
            "width": 20,
            "bd": 3
        })
        rpt_file_path_check_path_btn.grid({
            "row": 3,
            "column": 5,
            "padx": 5,
            "pady": 4
        })

        # ss
        dicttxt_file_path_label = Label(general_info_frame, {
            "width": 20,
            "padx": 5,
            "anchor": W,
            # "bg": self.colors.get("myblue"),
            "text": "Dict.txt file path:"
        })
        dicttxt_file_path_label.grid({
            "row": 4,
            "column": 4,
            "padx": 5,
            "pady": 4
        })

        dicttxt_file_path_entry = Entry(general_info_frame, {
            "bd": 2
        })
        dicttxt_file_path_entry.grid({
            "row": 4,
            "column": 5,
            "padx": 5,
            "pady": 4
        })

        dicttxt_file_path_browse_btn = Button(general_info_frame, {
            "text": "Check path",
            "width": 20,
            "bd": 3
        })
        dicttxt_file_path_browse_btn.grid({
            "row": 5,
            "column": 4,
            "padx": 5,
            "pady": 4
        })

        dicttxt_file_path_check_path_btn = Button(general_info_frame, {
            "text": "Check path",
            "width": 20,
            "bd": 3
        })
        dicttxt_file_path_check_path_btn.grid({
            "row": 5,
            "column": 5,
            "padx": 5,
            "pady": 4
        })
        # general_info_frame End

    def radiobutton_sellect(self):
        selection = "You selected the option " + str(self.radio_button_var.get())
        print(selection)

    def output_info(self):
        output_frame = Frame(self.tab1)
        output_frame.grid({
            "row": 1,
            "column": 0,
            "padx": 5,
            "pady": 4
        })
        output_label = Label(output_frame, {
            "width": 80,
            "padx": 10,
            "anchor": W,
            # "fg": self.colors.get("myblue"),
            "text": "Output",
            "font": 10
        })
        output_label.grid({
            "row": 0,
            "column": 0,
            "columnspan": 5,
            "padx": 10,
            "pady": 4
        })
        self.__textbox_with_scrollbar(output_frame)

    def single_prediction_info(self):
        single_prediction_frame = Frame(self.tab1)
        single_prediction_frame.grid({
            "row": 2,
            "column": 0,
            "padx": 5,
            "pady": 4
        })
        single_prediction_label = Label(single_prediction_frame, {
            "width": 21,
            "padx": 2,
            "anchor": W,
            # "fg": self.colors.get("myblue"),
            "text": "Single prediction",
            "font": 10
        })
        single_prediction_label.grid({
            "row": 0,
            "column": 0,
            "padx": 2,
            "pady": 4
        })
        sender_zip_code_label = Label(single_prediction_frame, {
            "width": 20,
            "padx": 2,
            "anchor": W,
            # "bg": self.colors.get("myblue"),
            "text": "Sender zipcode:"
        })
        sender_zip_code_label.grid({
            "row": 0,
            "column": 2,
            "padx": 2,
            "pady": 4
        })
        sender_zip_code_entry = Entry(single_prediction_frame, {
            "bd": 2
        })
        sender_zip_code_entry.grid({
            "row": 0,
            "column": 3,
            "padx": 2,
            "pady": 4
        })
        #
        receiver_zip_code_label = Label(single_prediction_frame, {
            "width": 20,
            "padx": 2,
            "anchor": W,
            # "bg": self.colors.get("myblue"),
            "text": "Receiver zipcode:"
        })
        receiver_zip_code_label.grid({
            "row": 0,
            "column": 4,
            "padx": 2,
            "pady": 4
        })
        receiver_zip_code_entry = Entry(single_prediction_frame, {
            "bd": 2
        })
        receiver_zip_code_entry.grid({
            "row": 0,
            "column": 5,
            "padx": 2,
            "pady": 4
        })
        make_prediction_btn = Button(single_prediction_frame, {
            "text": "Make prediction",
            "width": 15,
            "bd": 3,
            "command": self.testtakijaki
        })
        make_prediction_btn.grid({
            "row": 0,
            "column": 6,
            "padx": 2,
            "pady": 4
        })

    def actions_menu_info(self):
        actions_menu_info_frame = Frame(self.tab1)
        actions_menu_info_frame.grid({
            "row": 0,
            "column": 1,
            "padx": 5,
            "pady": 4
        })
        actions_menu_label = Label(actions_menu_info_frame, {
            "width": 20,
            "padx": 12,
            "anchor": W,
            # "fg": self.colors.get("myblue"),
            "text": "Actions menu",
            "font": 10
        })
        actions_menu_label.grid({
            "row": 0,
            "column": 0,
            "padx": 2,
            "pady": 8
        })

        create_database_btn = Button(actions_menu_info_frame, {
            "text": "Create database",
            "width": 30,
            "bd": 3
        })
        create_database_btn.grid({
            "row": 1,
            "column": 0,
            "padx": 2,
            "pady": 1
        })

        insert_dictionary_btn = Button(actions_menu_info_frame, {
            "text": "Insert dictionary data from txt file",
            "width": 30,
            "bd": 3
        })
        insert_dictionary_btn.grid({
            "row": 2,
            "column": 0,
            "padx": 2,
            "pady": 1
        })

        update_dictionary_from_missing_zip_btn = Button(actions_menu_info_frame, {
            "text": "Update dictionary from missing file",
            "width": 30,
            "bd": 3
        })
        update_dictionary_from_missing_zip_btn.grid({
            "row": 3,
            "column": 0,
            "padx": 2,
            "pady": 1
        })
        insert_learning_data_from_rpt_file_btn = Button(actions_menu_info_frame, {
            "text": "Insert learning data from rpt fle",
            "width": 30,
            "bd": 3
        })
        insert_learning_data_from_rpt_file_btn.grid({
            "row": 4,
            "column": 0,
            "padx": 2,
            "pady": 1
        })

        save_model_btn = Button(actions_menu_info_frame, {
            "text": "Save model",
            "width": 30,
            "bd": 3
        })
        save_model_btn.grid({
            "row": 5,
            "column": 0,
            "padx": 2,
            "pady": 1
        })
        #

    def models_list_info(self):
        models_list_info_frame = Frame(self.tab1)
        models_list_info_frame.grid({
            "row": 1,
            "rowspan": 2,
            "column": 1,
            "padx": 5,
            "pady": 4
        })
        actions_menu_label = Label(models_list_info_frame, {
            "width": 20,
            "padx": 2,
            "anchor": W,
            # "fg": self.colors.get("myblue"),
            "text": "Models list",
            "font": 10
        })
        actions_menu_label.grid({
            "row": 0,
            "column": 0,
            "padx": 2,
            "pady": 8
        })
        listBox1 = Listbox(models_list_info_frame, {
            "height": 16,
            "width": 35
        })
        listBox1.insert(1, "Temp33")
        listBox1.insert(2, "Knn45")

        listBox1.grid({
            "row": 1,
            "column": 0,
            "padx": 2,
            "pady": 8
        })
        choose_models_path = Button(models_list_info_frame, {
            "text": "Choose models path",
            "width": 30,
            "bd": 3
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
        currently_selected_label_entry = Entry(models_list_info_frame, {
            "bd": 2,
            "width": 35,
            "state": DISABLED
        })
        currently_selected_label_entry.grid({
            "row": 4,
            "column": 0,
            "padx": 10,
            "pady": 4
        })


    def testtakijaki(self):
        self.text.config(state=NORMAL)
        self.text.delete('1.0', END)
        # self.text.insert(INSERT, self.e1.get())

        mltemp = MachineLearning()
        dbc = DBConnector()
        cnx_pool = dbc.create_connection(32)

        completed_table = Completed_Table(cnx_pool)
        records = completed_table.collect_data(0, 1000)

        x_train, x_test, y_train, y_test = mltemp.split_data(records)

        model = mltemp.load_model("Models/TestKnnSave.sav")
        prediction = model.predict(x_test)

        epsilon = 12  # number of hours
        correct_predictions = 0
        all_predictions = 0

        for x in range(len(prediction)):
            if math.fabs(prediction[x] - y_test[x]) < epsilon:
                correct_predictions = correct_predictions + 1
            all_predictions = all_predictions + 1
            self.text.insert(INSERT, "Predicted: {} Data: {} Actual: {} \n".format(prediction[x], x_test[x], y_test[x]))

        self.text.insert(INSERT, "\nSelf made accuracy calculators: \n")
        self.text.insert(INSERT, "Prediction is classified as correct when belongs to range: \n")
        self.text.insert(INSERT, "from actual_value - {}h to actual_value + {}h \n".format(epsilon, epsilon))
        self.text.insert(INSERT, "Classification accuracy = {} \n".format(correct_predictions / all_predictions))
        self.text.config(state=DISABLED)

    def __textbox_with_scrollbar(self, tab):
        self.frameTemp = Frame(tab, {
            "height": 50,
            "width": 125
        })
        self.frameTemp.grid(row=1, column=0, sticky=W, padx=2, pady=2)
        self.text = Text(self.frameTemp, {
            "height": 20,
            "width": 112,
        })
        self.text.grid(row=0, column=0, sticky=NW, padx=2, pady=2)
        scrollb = Scrollbar(self.frameTemp, command=self.text.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        self.text['yscrollcommand'] = scrollb.set
        self.text.config(state=DISABLED)

    def __allListBox(self):
        listBox1 = Listbox(self)
        listBox1.insert(1, "Test1")
        listBox1.insert(2, "Test2")

        listBox1.grid(row=3, column=1, sticky=W, pady=2)

    def __addMenu(self):
        menubar = Menu(self)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.donothing)
        filemenu.add_command(label="Open", command=self.donothing)
        filemenu.add_command(label="Save", command=self.donothing)
        filemenu.add_command(label="Save as...", command=self.donothing)
        filemenu.add_command(label="Close", command=self.donothing)

        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Undo", command=self.donothing)

        editmenu.add_separator()

        editmenu.add_command(label="Cut", command=self.donothing)
        editmenu.add_command(label="Copy", command=self.donothing)
        editmenu.add_command(label="Paste", command=self.donothing)
        editmenu.add_command(label="Delete", command=self.donothing)
        editmenu.add_command(label="Select All", command=self.donothing)

        menubar.add_cascade(label="Edit", menu=editmenu)
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=self.donothing)
        helpmenu.add_command(label="About...", command=self.donothing)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.master.config(menu=menubar)
