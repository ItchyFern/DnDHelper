import tkinter as tk
from tkinter.filedialog import askopenfilename
import pyperclip
import util
import re, json

class Window():
    def __init__(self):
        self.window = tk.Tk()
        self.initialize()
        self.window.mainloop()


    def loadPreferences(self):
        try:
            #print("entered preference loading")
            with open(".preferences", "r") as readfile:
                #print ("opened file for preferences")
                for line in readfile.readlines():
                    regex = re.search("(\w*)\s*=\s*\"(.*?)\"", line)
                    print (regex.group(1), "=", regex.group(2))
                    self.preferences[regex.group(1)] = regex.group(2)

        except Exception as e:
            print("failed to load preferences:", e)

    def openData(self):
        datafile = askopenfilename(filetypes=(("Character Files", "*.json"),
                                                  ("All files", "*.*") ))
        print (datafile, " <- location selected")
        return datafile

    def loadData(self, datafile):
        try:
            with open(datafile, "r") as readfile:
                self.data = json.load(readfile)

            print ("getting important info from data...")
            # grab only the important data for this program
            self.data = self.data["sheet_data"]["jsondata"]

            print ("data loaded successfully")
        except:
            print ("data not loaded successfully")


    def attack(self):
        pyperclip.copy(util.attack(self.data, self.preferences["weapon"]))

    def equip(self):
        #initialize dialog box and title
        selectdialog = tk.Toplevel()
        selectdialog.title("Choose a weapon")

        #initialize weapon choices
        wi = util.getWeaponInfo(self.data)
        print (wi)
        for weapon in wi:
            print("looking at weapons")
            name = weapon
            info = []
            for suffix in ["AB", "Damage", "Type"]:
                try:
                    info.append(str(wi[weapon][suffix]))
                except:
                    info.append("N/A")

            tk.Button(selectdialog,
                      text = "{:>20} | {:20} | {:8} | {:9}".format(name,
                                                                  info[0],
                                                                  info[1],
                                                                  info[2]),
                      command = lambda w = weapon: set(w)).pack(fill="x")

        def set(weap):
            self.preferences["weapon"] = weap
            selectdialog.destroy()

    def save(self):
        with open(".preferences", "r+") as f:
            data = f.read()
            f.seek(0)
            for key in self.preferences:
                print ("{} = \"{}\"\n".format(key, self.preferences[key]))
                f.write("{} = \"{}\"\n".format(key, self.preferences[key]))
            f.truncate()
        print ("saved successfully")

    def initialize(self):
        #initialize important variables
        self.data = ""
        self.preferences = {}

        #initialize and pack frames
        self.titleframe = tk.Frame(self.window)
        self.titleframe.pack()

        self.optionsframe = tk.Frame(self.window)
        self.optionsframe.pack(fill = "x")

        # Buttons in the options frame
        self.attbutton = tk.Button(self.optionsframe,
                                   text = "Attack",
                                   command = lambda:self.attack())
        self.hitbutton = tk.Button(self.optionsframe,
                                   text = "Hit",
                                   command = lambda:self.hit())
        self.skibutton = tk.Button(self.optionsframe,
                                   text = "Skill Check",
                                   command = lambda:self.skill())
        self.equbutton = tk.Button(self.optionsframe,
                                   text = "Equip",
                                   command = lambda:self.equip())
        self.savbutton = tk.Button(self.optionsframe,
                                   text = "Save",
                                   command = lambda:self.save())

        #pack all the Buttons
        self.attbutton.pack(fill="x")
        self.hitbutton.pack(fill="x")
        self.skibutton.pack(fill="x")
        self.equbutton.pack(fill="x")
        self.savbutton.pack(fill="x")

        #check preferences file
        self.loadPreferences()

        datafile = ""
        try:
            #check if there is a data preference in preference file
            if self.preferences["data"] != "":
                datafile = self.preferences["data"]
        except:
            # if nothing in preferences file ask to open json file
            print("datafile not found in preferences")
            self.preferences["data"] = self.openData()

        #load datafile
        self.loadData(self.preferences["data"])



window = Window()
