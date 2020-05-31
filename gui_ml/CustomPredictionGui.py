from tkinter import ttk
from tkinter import filedialog
from ml.MachineLearning import MachineLearning
import numpy
import sklearn
from sklearn.neighbors import KNeighborsClassifier
import gui_ml.ModelsListGui as Models_list_gui
import data_logic.Utils as ut
import db_tables.Postcode_Table as Postcode_Table
from tkinter import *
import data_db_connector.DBConnector as dbConn


class CustomPredictionGui:

    def __init__(self, model_gui: Models_list_gui.ModelsListGui):
        self.model_gui = model_gui

    def create_custom_prediction_frame(self, root):
        single_prediction_frame = Frame(root)
        single_prediction_label = Label(single_prediction_frame, {
            "width": 74,
            "height": 2,
            "padx": 2,
            "anchor": W,
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
            "text": "Sender zipcode: [00-000]"
        })
        sender_zip_code_label.grid({
            "row": 3,
            "column": 1,
            "padx": 2,
            "pady": 4
        })
        self.sender_zip_code_entry = Entry(single_prediction_frame, {
            "bd": 2
        })
        self.sender_zip_code_entry.grid({
            "row": 3,
            "column": 2,
            "padx": 2,
            "pady": 4
        })
        #
        receiver_zip_code_label = Label(single_prediction_frame, {
            "width": 20,
            "padx": 2,
            "anchor": W,
            "text": "Receiver zipcode: [00-000]"
        })
        receiver_zip_code_label.grid({
            "row": 3,
            "column": 3,
            "padx": 2,
            "pady": 4
        })
        self.receiver_zip_code_entry = Entry(single_prediction_frame, {
            "bd": 2
        })
        self.receiver_zip_code_entry.grid({
            "row": 3,
            "column": 4,
            "padx": 2,
            "pady": 4
        })

        # data picker
        date_label = Label(single_prediction_frame, {
            "width": 20,
            "padx": 2,
            "anchor": W,
            "text": "Data (Y-M-D) [0000-00-00]"
        })
        date_label.grid({
            "row": 4,
            "column": 1,
            "padx": 2,
            "pady": 4
        })
        self.date_entry = Entry(single_prediction_frame, {
            "bd": 2
        })
        self.date_entry.grid({
            "row": 4,
            "column": 2,
            "padx": 2,
            "pady": 4
        })

        time_label = Label(single_prediction_frame, {
            "width": 20,
            "padx": 2,
            "anchor": W,
            "text": "Time (H:M:S) [00:00:00]"
        })
        time_label.grid({
            "row": 4,
            "column": 3,
            "padx": 2,
            "pady": 4
        })
        self.time_entry = Entry(single_prediction_frame, {
            "bd": 2
        })
        self.time_entry.grid({
            "row": 4,
            "column": 4,
            "padx": 2,
            "pady": 4
        })

        self.select_radio = IntVar()
        R1 = Radiobutton(single_prediction_frame, text="DataBase", variable=self.select_radio, value=1)
        R1.grid({
            "row": 4,
            "column": 5,
            "padx": 2,
            "pady": 4
        })
        R1.select()
        R2 = Radiobutton(single_prediction_frame, text="GEOPY", variable=self.select_radio, value=2)
        R2.grid({
            "row": 4,
            "column": 6,
            "padx": 2,
            "pady": 4
        })
        R2.deselect()

        make_prediction_btn = Button(single_prediction_frame, {
            "text": "Make prediction",
            "width": 20,
            "bd": 3,
            "command": self.predit
        })
        make_prediction_btn.grid({
            "row": 6,
            "column": 6,
            "padx": 2,
            "pady": 4
        })

        return single_prediction_frame

    def predit(self):
        cordsSenderLatitude, cordsSenderLongitude, cordsReceiverLatitude, cordsReceiverLongitude = 0, 0, 0, 0
        sender_name = ""
        receiver_name = ""

        mltemp = MachineLearning()
        model = mltemp.load_model("{}".format(self.model_gui.dirpath + "/" + self.model_gui.selected))
        self.text.config(state=NORMAL)
        self.text.delete('1.0', END)
        senderZipCode0 = int(str(self.sender_zip_code_entry.get()).split("-")[0][0])
        senderZipCode1 = int(str(self.sender_zip_code_entry.get()).split("-")[0][1])
        receiverZipCode0 = int(str(self.receiver_zip_code_entry.get()).split("-")[0][0])
        receiverZipCode1 = int(str(self.receiver_zip_code_entry.get()).split("-")[0][1])

        date: str = str(self.date_entry.get()).replace(" ", "")
        time: str = str(self.time_entry.get()).replace(" ", "")
        date_string = date + " " + time + ".000"
        unixTime = ut.Utils.convert_to_unix_time(date_string)

        if str(self.select_radio.get()) == "2":
            self.text.insert(INSERT, "From Geopy\n\n")
            cordsSenderLatitude, cordsSenderLongitude = ut.Utils.convert_postcode_to_cords(
                self.sender_zip_code_entry.get())
            cordsReceiverLatitude, cordsReceiverLongitude = ut.Utils.convert_postcode_to_cords(
                self.receiver_zip_code_entry.get())
        else:
            self.text.insert(INSERT, "From DataBase:\n\n")
            dcConTemp = dbConn.DBConnector()
            postcode_table = Postcode_Table.Postcode_Table(dcConTemp.create_connection(1))
            country_code: str = "PL"
            senderCord = postcode_table.get_coordinates(country_code, self.sender_zip_code_entry.get())
            receiverCord = postcode_table.get_coordinates(country_code, self.receiver_zip_code_entry.get())
            cordsSenderLatitude = senderCord['latitude']
            cordsSenderLongitude = senderCord['longitude']
            cordsReceiverLatitude = receiverCord['latitude']
            cordsReceiverLongitude = receiverCord['longitude']
            sender_name = senderCord['placeName']
            receiver_name = receiverCord['placeName']

        distance = ut.Utils.convert_cords_to_distance(cordsSenderLatitude, cordsSenderLongitude,
                                                      cordsReceiverLatitude, cordsReceiverLongitude)
        self.text.insert(INSERT, "Distance:           {}\n".format(distance))
        self.text.insert(INSERT,
                         "Sender name:        {} \nReceiver name:      {} \n".format(sender_name, receiver_name))
        self.text.insert(INSERT, "Order date:         {}\n".format(
            ut.Utils.convert_to_normal_time(unixTime).strftime("%d/%m/%Y %H:%M:%S")))
        temp = numpy.array(
            [unixTime, distance, senderZipCode0, senderZipCode1, receiverZipCode0, receiverZipCode1]).reshape(-1, 6)
        prediction = model.predict(temp)
        for x in range(len(prediction)):
            temp_unix = unixTime + prediction[x] * 3600
            self.text.insert(INSERT, "Predicted delivery: {}\n".format(
                ut.Utils.convert_to_normal_time(temp_unix).strftime("%d/%m/%Y %H:%M:%S")))
            self.text.insert(INSERT, "Predicted hour:     {} h\n".format(prediction[x]))
            self.text.insert(INSERT, "\nRaw data: Predicted: {} Data: {} \n".format(prediction[x], temp[x]))
        self.text.config(state=DISABLED)

    def selected_button(self, sel_numb: int):
        self.select_radio = sel_numb

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
