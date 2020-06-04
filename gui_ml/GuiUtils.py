from tkinter import ttk
from tkinter import filedialog
from tkinter import *

class GuiUtils:
    def test_frame(self, root):
        tempFrame = Frame(root)
        l1 = Label(tempFrame, {
            "text": "Elo TESTY UUU"
        })
        l1.pack()
        return tempFrame
