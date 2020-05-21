from tkinter import ttk
from tkinter import filedialog
from tkinter import *


class DatabaseSetupGui:

    def create_database_setup_frame(self, root):
        database_setup_frame = Frame(root)
        model_list_label = Label(database_setup_frame, {
            "width": 18,
            "padx": 2,
            "anchor": W,
            "text": "Database setup",
            "font": 10
        })
        model_list_label.grid({
            "row": 0,
            "column": 0,
            "padx": 2,
            "pady": 8
        })

        label_names = ("Database host:", "Database name:", "User:", "Password:")
        for i in range(1, 5):
            l1 = Label(database_setup_frame, {
                "width": 12,
                "padx": 5,
                "anchor": W,
                "text": label_names[i - 1]
            })
            l1.grid({
                "row": i,
                "column": 0,
                "padx": 5,
                "pady": 4
            })

        self.db_host_entry = Entry(database_setup_frame, {
            "bd": 2
        })
        self.db_host_entry.grid({
            "row": 1,
            "column": 1,
            "padx": 5,
            "pady": 4
        })
        db_name_entry = Entry(database_setup_frame, {
            "bd": 2
        })
        db_name_entry.grid({
            "row": 2,
            "column": 1,
            "padx": 5,
            "pady": 4
        })
        db_user_entry = Entry(database_setup_frame, {
            "bd": 2
        })
        db_user_entry.grid({
            "row": 3,
            "column": 1,
            "padx": 5,
            "pady": 4
        })
        db_password_entry = Entry(database_setup_frame, {
            "bd": 2
        })
        db_password_entry.grid({
            "row": 4,
            "column": 1,
            "padx": 5,
            "pady": 4
        })

        test_connection_bttn = Button(database_setup_frame, {
            "text": "Test connection",
            "width": 30,
            "bd": 3
        })
        test_connection_bttn.grid({
            "row": 5,
            "column": 0,
            "columnspan": 2,
            "padx": 5,
            "pady": 4
        })
        rpt_file_path_label = Label(database_setup_frame, {
            "width": 20,
            "padx": 5,
            "anchor": W,
            "text": "RPT file path:"
        })
        rpt_file_path_label.grid({
            "row": 2,
            "column": 2,
            "padx": 5,
            "pady": 4
        })

        rpt_file_path_entry = Entry(database_setup_frame, {
            "bd": 2
        })
        rpt_file_path_entry.grid({
            "row": 2,
            "column": 3,
            "padx": 5,
            "pady": 4
        })

        rpt_file_path_browse_btn = Button(database_setup_frame, {
            "text": "Browse",
            "width": 30,
            "bd": 3
        })
        rpt_file_path_browse_btn.grid({
            "row": 3,
            "column": 2,
            "columnspan": 2,
            "padx": 5,
            "pady": 4
        })

        dicttxt_file_path_label = Label(database_setup_frame, {
            "width": 20,
            "padx": 5,
            "anchor": W,
            "text": "Dict.txt file path:"
        })
        dicttxt_file_path_label.grid({
            "row": 4,
            "column": 2,
            "padx": 5,
            "pady": 4
        })

        dicttxt_file_path_entry = Entry(database_setup_frame, {
            "bd": 2
        })
        dicttxt_file_path_entry.grid({
            "row": 4,
            "column": 3,
            "padx": 5,
            "pady": 4
        })

        dicttxt_file_path_browse_btn = Button(database_setup_frame, {
            "text": "Browse",
            "width": 30,
            "bd": 3
        })
        dicttxt_file_path_browse_btn.grid({
            "row": 5,
            "column": 2,
            "columnspan": 2,
            "padx": 5,
            "pady": 4
        })

        return database_setup_frame
