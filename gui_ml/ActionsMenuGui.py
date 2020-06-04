from tkinter import *


class ActionsMenuGui:

    def create_actions_menu_frame(self, root):
        actions_menu_info_frame = Frame(root)
        actions_menu_label = Label(actions_menu_info_frame, {
            "width": 20,
            "padx": 12,
            "anchor": W,
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
            "pady": 5
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
            "pady": 5
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
            "pady": 5
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
            "pady": 5
        })
        return actions_menu_info_frame
