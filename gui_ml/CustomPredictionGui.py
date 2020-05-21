from tkinter import ttk
from tkinter import filedialog
from ml.MachineLearning import MachineLearning
import numpy
import sklearn
from sklearn.neighbors import KNeighborsClassifier
import gui_ml.ModelsListGui as Models_list_gui
from tkinter import *


class CustomPredictionGui:

    def __init__(self, model_gui: Models_list_gui.ModelsListGui):
        self.model_gui = model_gui

    def create_custom_prediction_frame(self, root):
        single_prediction_frame = Frame(root)
        single_prediction_label = Label(single_prediction_frame, {
            "width": 40,
            "padx": 2,
            "anchor": W,
            # "fg": self.colors.get("myblue"),
            "text": "Custom prediction",
            "font": 10
        })
        single_prediction_label.grid({
            "row": 0,
            "column": 0,
            "columnspan": 10,
            "padx": 4,
            "pady": 4
        })
        self.__textbox_with_scrollbar(single_prediction_frame).grid({
            "row": 1,
            "column": 0,
            "columnspan": 10,
            "padx": 4,
            "pady": 4
        })
        sender_zip_code_label = Label(single_prediction_frame, {
            "width": 20,
            "padx": 2,
            "anchor": W,
            "text": "Sender zipcode:"
        })
        sender_zip_code_label.grid({
            "row": 3,
            "column": 2,
            "padx": 2,
            "pady": 4
        })
        self.sender_zip_code_entry = Entry(single_prediction_frame, {
            "bd": 2
        })
        self.sender_zip_code_entry.grid({
            "row": 3,
            "column": 3,
            "padx": 2,
            "pady": 4
        })
        #
        receiver_zip_code_label = Label(single_prediction_frame, {
            "width": 20,
            "padx": 2,
            "anchor": W,
            "text": "Receiver zipcode:"
        })
        receiver_zip_code_label.grid({
            "row": 3,
            "column": 4,
            "padx": 2,
            "pady": 4
        })
        self.receiver_zip_code_entry = Entry(single_prediction_frame, {
            "bd": 2
        })
        self.receiver_zip_code_entry.grid({
            "row": 3,
            "column": 5,
            "padx": 2,
            "pady": 4
        })
        unix_time_create_shipment_label = Label(single_prediction_frame, {
            "width": 20,
            "padx": 2,
            "anchor": W,
            "text": "Unix time shipment create:"
        })
        unix_time_create_shipment_label.grid({
            "row": 4,
            "column": 2,
            "padx": 2,
            "pady": 4
        })
        self.unix_time_create_shipment_entry = Entry(single_prediction_frame, {
            "bd": 2
        })
        self.unix_time_create_shipment_entry.grid({
            "row": 4,
            "column": 3,
            "padx": 2,
            "pady": 4
        })
        distance_label = Label(single_prediction_frame, {
            "width": 20,
            "padx": 2,
            "anchor": W,
            "text": "Distance:"
        })
        distance_label.grid({
            "row": 4,
            "column": 4,
            "padx": 2,
            "pady": 4
        })
        self.distance_entry = Entry(single_prediction_frame, {
            "bd": 2
        })
        self.distance_entry.grid({
            "row": 4,
            "column": 5,
            "padx": 2,
            "pady": 4
        })
        make_prediction_btn = Button(single_prediction_frame, {
            "text": "Make prediction",
            "width": 20,
            "bd": 3,
            "command": self.predit
        })
        make_prediction_btn.grid({
            "row": 5,
            "column": 5,
            "padx": 2,
            "pady": 4
        })

        return single_prediction_frame

    def predit(self):
        mltemp = MachineLearning()
        model = mltemp.load_model("{}".format(self.model_gui.dirpath+"/"+self.model_gui.selected))
        # model = mltemp.load_model("Models/TestKnnSave.sav")
        arrayN = numpy.empty(0)
        self.text.config(state=NORMAL)
        self.text.delete('1.0', END)
        unixTime = int(self.unix_time_create_shipment_entry.get())
        distance = int(self.distance_entry.get())
        senderZipCode0 = int(str(self.sender_zip_code_entry.get()).split("-")[0][0])
        senderZipCode1 = int(str(self.sender_zip_code_entry.get()).split("-")[0][1])
        receiverZipCode0 = int(str(self.receiver_zip_code_entry.get()).split("-")[0][0])
        receiverZipCode1 = int(str(self.receiver_zip_code_entry.get()).split("-")[0][1])
        temp = numpy.array(
            [unixTime, distance, senderZipCode0, senderZipCode1, receiverZipCode0, receiverZipCode1]).reshape(-1, 6)
        # temp = numpy.array([1582256841, 300, 9, 0, 7, 1]).reshape(-1, 6)
        prediction = model.predict(temp)
        for x in range(len(prediction)):
            self.text.insert(INSERT, "Predicted: {} Data: {} \n".format(prediction[x], temp[x]))
        self.text.config(state=DISABLED)

    def __textbox_with_scrollbar(self, tab):
        frameTemp = Frame(tab, {
            "height": 40,
            "width": 111,
        })
        frameTemp.grid(row=1, column=0, sticky=W, padx=2, pady=2)
        self.text = Text(frameTemp, {
            "height": 23,
            "width": 111,
        })
        self.text.grid(row=0, column=0, sticky=NW, padx=2, pady=2)
        scrollb = Scrollbar(frameTemp, command=self.text.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        self.text['yscrollcommand'] = scrollb.set
        self.text.config(state=DISABLED)
        return frameTemp
