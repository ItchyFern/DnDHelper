import tkinter as tk
import util

class Window():
    def __init__(self):
        self.window = tk.Tk()
        self.initialize()
        self.window.mainloop()

    def initialize(self):
        self.titleframe = tk.Frame(self.window)
        self.titleframe.pack()

        self.optionsframe = tk.Frame(self.window)
        self.optionsframe.pack(fill = "x")

        # Buttons in the options frame
        self.attbutton = tk.Button(self.optionsframe, \
                                   text = "Attack", \
                                   command = lambda:self.attack())
        self.hitbutton = tk.Button(self.optionsframe \
                                   text = "Hit", \
                                   command = lambda:self.hit())
        self.skibutton = tk.Button(self.optionsframe \
                                   text = "Skill Check", \
                                   command = lambda:self.skill())
        self.equbutton = tk.Button(self.optionsframe \
                                   text = "Equip", \
                                   command = lambda:self.equip())

        #pack all the Buttons
        self.attbutton.pack()
        self.hitbutton.pack()
        self.skibutton.pack()
        self.equbutton.pack()

window = Window()
