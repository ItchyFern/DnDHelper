

import json, os
from rofi import Rofi

def getBasicInfo(data):
    ret = {}
    ret["Name"] = data["Name"]
    ret["Alignment"] = data["Alignment"]
    ret["Race"] = data["Race"]
    ret["Campaign"] = data["Campaign"]
    ret["Age"] = data["Age"]
    ret["Height"] = data["Height"]
    ret["Weight"] = data["Weight"]
    ret["Eyes"] = data["Eyes"]
    ret["Hair"] = data["Hair"]
    ret["HP"] = data["HP"]
    ret["Deity"] = data["Deity"]
    return ret

def getWeaponInfo(data):
    ret = {}
    #possible values per weapon
    values = ["AB", "Damage", "Crit", "Range", "Ammo", "Weight", "Size", "Type"]
    #check the 4 slots for weapons
    for wnum in range(1, 5):
        weaponstr = "Weapon{}".format(wnum)
        #use try catch incase weapon not available
        try:
            #set key to be name of the weapon
            key = data[weaponstr]

            value = {}
            for suffix in values:
                #use try catch incase modifier not available
                try:
                    value[suffix] = data[weaponstr + suffix]
                except:
                    print (key + " modifier " + suffix + " not found.")

            #set value to dict containing the info
            ret[key] = value
        except:
            print(weaponstr + " not found.")
    return ret

def getSkillInfo(data):
    ret = {}
    #possible values per skill
    values = ["Ab", "CC", "AbMod", "Rank", "MiscMod", "Mod"]
    #check the first 38 skills (in base 3.5e)
    for snum in range(1, 39):
        skillstr = "Skill{:0>2}".format(snum)
        #use try catch incase skill not available
        try:
            #set key to be name of the skill
            key = data[skillstr]

            value = {}
            for suffix in values:
                # use try catch incase modifier not available
                try:
                    value[suffix] = data[skillstr + suffix]
                except:
                    print (key + " modifier " + suffix + " not found.")


            #set value to dict containing the info
            ret[key] = value
        except:
            print(skillstr + " not found.")
    return ret

def attack(weapon, stats):
    pass
    
def run():
    with open("Seth's Marshal-2019-12-19.json", "r") as readfile:
        data = json.load(readfile)

    # grab only the important data for this program
    data = data["sheet_data"]["jsondata"]
    print (getWeaponInfo(data))
    rofi(data)

def rofi(data):
    # https://github.com/bcbnz/python-rofi
    r = Rofi()
    r.text_entry('What is your name?')

if __name__ == "__main__":
    run()
