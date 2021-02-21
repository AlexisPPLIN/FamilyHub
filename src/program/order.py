import random

def GenerateWeekProgramOrder(nbMembers):
    # Blank template
    week = {
        "lundi": {"Dish":-1,"Dog food":-1,"Trash":-1,"Vacuum":-1,"Table":-1},
        "mardi": {"Dish":-1,"Dog food":-1,"Trash":-1,"Vacuum":-1,"Table":-1},
        "mercredi": {"Dish":-1,"Dog food":-1,"Trash":-1,"Vacuum":-1,"Table":-1},
        "jeudi": {"Dish":-1,"Dog food":-1,"Trash":-1,"Vacuum":-1,"Table":-1},
        "vendredi": {"Dish":-1,"Dog food":-1,"Trash":-1,"Vacuum":-1,"Table":-1},
        "samedi": {"Dish":-1,"Dog food":-1,"Trash":-1,"Vacuum":-1,"Table":-1},
        "dimanche": {"Dish":-1,"Dog food":-1,"Trash":-1,"Vacuum":-1,"Table":-1},
    }

    # Choose starting number to generate week program
    start_number = random.randint(0,nbMembers-1)
    
    for day in week:
        index = start_number
        for task in week[day]:
            week[day][task] = index
            index += 1

            if index > nbMembers-1:
                index = 0
        
        start_number += 1
        if start_number > nbMembers-1:
            start_number = 0

    return week