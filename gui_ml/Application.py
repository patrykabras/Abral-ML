from tkinter import ttk
from tkinter import filedialog
from tkinter import *


import gui_ml.GuiUtils as guiU
import gui_ml.OutputGui as Output_gui
import gui_ml.CustomPredictionGui as Custom_prediction_gui
import gui_ml.ActionsMenuGui as Actions_menu_gui
import gui_ml.ModelsListGui as Models_list_gui
import gui_ml.GeneralInfoGui as General_info_gui
import gui_ml.DatabaseSetupGui as Database_setup_gui




class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.resolutions = {
            "width": 1250,
            "height": 800
        }
        self.colors = {
            "myblue": "#4eaef2",
            "mygreen": "#16db04",
            "myred": "#dd0202"
        }
        self.master.geometry("{}x{}".format(self.resolutions.get("width"), self.resolutions.get("height")))
        self.master.title("Abral - Projekt - Tracking z wykorzystaniem uczenia maszynowego")
        # self.master.iconphoto(False, PhotoImage(file='gui_ml/abral-icon.png'))
        self.master.call('wm', 'iconphoto', self.master._w, PhotoImage(file='gui_ml/abral-icon.png'))
        self.pack()
        self.master.configure(bg='blue')
        self.init_setup_frames()

    def init_setup_frames(self):
        self.create_style()
        self.init_custome_gui()
        self.create_notepad()
        self.createWidgets()

    def init_custome_gui(self):
        self.tempGuiU = guiU.GuiUtils()
        self.output_gui = Output_gui.OutputGui()
        self.models_list_gui = Models_list_gui.ModelsListGui()
        self.custome_prediction_gui = Custom_prediction_gui.CustomPredictionGui(self.models_list_gui)
        self.actions_menu_gui = Actions_menu_gui.ActionsMenuGui()
        self.general_info_gui = General_info_gui.GeneralInfoGui(self.output_gui)
        self.database_setup_gui = Database_setup_gui.DatabaseSetupGui()

    def donothing(self):
        print("Do nothing")

    def create_notepad(self):
        tabControl = ttk.Notebook(self, width=self.resolutions.get("width"), height=self.resolutions.get("height"))

        self.tab1 = ttk.Frame(tabControl)
        self.tab2 = ttk.Frame(tabControl)
        self.tab3 = ttk.Frame(tabControl)

        tabControl.add(self.tab3, text='Database logic')
        tabControl.add(self.tab1, text='Learn model')
        tabControl.add(self.tab2, text='Custom prediction')
        tabControl.pack({
            "side": LEFT,
            "fill": BOTH,
        })

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
                # "background": self.colors.get("myblue")
            }
            }
        })
        self.style.theme_use("MyStyle")

    def createWidgets(self):
        self.__addMenu()
        self.setup_tab1()
        self.setup_tab2()
        self.setup_tab3()

    def setup_tab1(self):
        self.general_info_gui.create_general_frame(self.tab1).grid({
            "row": 0,
            "column": 0,
            "padx": 4,
            "pady": 8
        })
        self.output_gui.create_output_frame(self.tab1).grid({
            "row": 1,
            "column": 0,
            "columnspan": 2,
            "padx": 4,
            "pady": 4
        })

    def setup_tab2(self):
        self.models_list_gui.create_models_list_frame(self.tab2).grid({
            "row": 0,
            # "rowspan": 2,
            "column": 1,
            "padx": 4,
            "pady": 4
        })
        custom_prediction_gui = Custom_prediction_gui.CustomPredictionGui(self.models_list_gui)
        custom_prediction_gui.create_custom_prediction_frame(self.tab2).grid({
            "row": 0,
            "column": 0,
            "padx": 4,
            "pady": 4
        })

    def setup_tab3(self):
        self.database_setup_gui.create_database_setup_frame(self.tab3).grid({
            "row": 0,
            "column": 0,
            "padx": 10,
            "pady": 10
        })
        self.actions_menu_gui.create_actions_menu_frame(self.tab3).grid({
            "row": 0,
            "column": 1,
            "padx": 10,
            "pady": 10
        })

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
