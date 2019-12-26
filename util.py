

import json, os, re
from rofi import Rofi
import pyperclip

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
                    # print (key + " modifier " + suffix + " not found.")
                    pass
            #set value to dict containing the info
            ret[key] = value
        except:
            # print(weaponstr + " not found.")
            pass
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
                    # print (key + " modifier " + suffix + " not found.")
                    pass


            #set value to dict containing the info
            ret[key] = value
        except:
            # print(skillstr + " not found.")
            pass
    return ret

def getAbilityInfo(data):
    ret = {}
    #possible keys (abilities)
    keys = ["Str", "Dex", "Con", "Int", "Wis", "Cha"]
    values = ["Score", "Mod"]
    for key in keys:
        #use try catch incase ability not available
        try:
            #set key to be name of the skill
            value = {}
            value[values[0]] = data[key]
            value[values[1]] = data[key + "Mod"]

            #set value to dict containing the info
            ret[key] = value
        except:
            print(key + " not found.")
    return ret

def attack(data, weapon):
    #get weapon Type
    wtype, wab = getWeaponInfo(data)[weapon]["Type"], getWeaponInfo(data)[weapon]["AB"]
    #get strength and dexterity modifiers
    str, dex = getAbilityInfo(data)["Str"]["Mod"], getAbilityInfo(data)["Dex"]["Mod"]
    # if weapon type is melee set mod to str mod
    if wtype.strip().lower() == "melee":
        mod = str
    # if weapon type is ranged set mod to dex mod
    elif wtype.strip().lower() == "ranged" or wtype.strip().lower() == "range":
        mod = dex
    # if weapon type is unknown, ask user for entry
    else:
        print("unknown weapon type")
        uc = input ("melee or ranged (m/r) -> ")
        if uc == "m":
            mod = str
        elif uc == "r":
            mod = dex

    string = "/r 1d20"
    regex = re.match(r"\+\s*(\d*)", wab.strip())
    if (regex != None):
        totmod = int(regex.group(0)) + int(mod)
        string += " + {}".format(totmod)
    return string

def hit(data, weapon):
    wi = getWeaponInfo(data)[weapon]
    wtype, wab = wi["Type"], wi["AB"]
    #get strength modifier
    str = getAbilityInfo(data)["Str"]["Mod"]
    # if weapon type is melee set mod to str mod
    if wtype.strip().lower() == "melee":
        mod = str
    # if weapon type is ranged set mod to 0
    elif wtype.strip().lower() == "ranged" or wtype.strip().lower() == "range":
        mod = 0
    # [num]d[num]+[num]
    # ex. 1d10+3
    regex = re.search(r"(\d*)\s*[d,D]\s*(\d*)\s*\+*\s*(\d*)", wi["Damage"])
    string = "/r "
    #print (wi["Damage"])
    if regex.group(1) != None:
        #print (regex.group(1))
        string += regex.group(1)
    if regex.group(2) != None:
        #print (regex.group(2))
        string += "d" + regex.group(2)
    if regex.group(3) != "":
        #print (regex.group(3))
        string += " + {}".format(int(mod) + int(regex.group(3)))
    return string

def skillcheck(data, s):
    str = "/r 1d20 "
    if s == "":
        for skill in getSkillInfo(data):
            print (skill)
    else:
        for skill in getSkillInfo(data):
            if s.lower() in skill.lower():
                str += "+ {}".format(getSkillInfo(data)[skill]["Mod"])
                break
        return str

def save(data):
    pass


def run():
    with open("Seth's Marshal-2019-12-19.json", "r") as readfile:
        data = json.load(readfile)


    # grab only the important data for this program
    data = data["sheet_data"]["jsondata"]

    # initialize equipped weapon
    eweapon = ""
    eweapon = "Ranseur"

    while (True):

        command = input("-> ")
        #check to make sure weapon is equipped
        if eweapon != "":
            # attack roll, ask for hit after
            if command in "attack" or command == "":
                cb = attack (data, eweapon)
                print ('"{}" copied to clipboard'.format(cb))
                pyperclip.copy(cb)

                uc = input ("hit?(y/N) -> ")
                if uc.lower() == 'y':
                    cb = hit(data, eweapon)
                    print ('"{}" copied to clipboard'.format(cb))
                    pyperclip.copy(cb)
                continue

            # hit roll
            elif command in "hit":
                cb = hit(data, eweapon)
                print ('"{}" copied to clipboard'.format(cb))
                pyperclip.copy(cb)
                continue

        # equip weapon
        if command in "equip weapon":
            for key in getWeaponInfo(data):
                print (key)
            eweapon = input("choose weapon: ")
            for weapname in getWeaponInfo(data):
                if eweapon.lower() in weapname.lower():
                    eweapon = weapname
                    break
            print ("You equip {}".format(eweapon))


        elif command in "skills":
            cb = skillcheck(data)
            print ('"{}" copied to clipboard'.format(cb))
            pyperclip.copy(cb)

        elif command in "save":
            cb = save(data)
            print ('"{}" copied to clipboard'.format(cb))
            pyperclip.copy()


        elif command == "exit":
            print("Exiting...")
            break



def rofi(data):
    # https://github.com/bcbnz/python-rofi
    r = Rofi()
    r.text_entry('What is your name?')

if __name__ == "__main__":
    run()
