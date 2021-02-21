import os
from datetime import date

from ..program.day import GetDayProgram
from .util import ImageFont, Image, DrawText, fontdir, imgdir

def DrawTasks(Himage):
    print("Draw day tasks")
    today_program = GetDayProgram()
    current_day = date.today().strftime("%A")

    RobotoLight36 = ImageFont.truetype(os.path.join(fontdir, 'Roboto/Roboto-Light.ttf'), 36)
    RobotoLight14 = ImageFont.truetype(os.path.join(fontdir, 'Roboto/Roboto-Light.ttf'), 14)
    DrawText(Himage,'sans / avec les filles',RobotoLight14,113,133)

    # Dishwasher
    dishwasherImg = Image.open(os.path.join(imgdir,'tasks/dishwasher.png'))
    Himage.paste(dishwasherImg,(12,133),dishwasherImg)
    text = today_program['normal'][str(current_day)]['Dish']+" / "+today_program['weekend'][str(current_day)]['Dish']
    DrawText(Himage,text,RobotoLight36,110,151)

    # Dog food
    dogFoodImg = Image.open(os.path.join(imgdir,'tasks/dog-food.png'))
    Himage.paste(dogFoodImg,(12,210),dogFoodImg)
    text = today_program['normal'][str(current_day)]['Dog food']+" / "+today_program['weekend'][str(current_day)]['Dog food']
    DrawText(Himage,text,RobotoLight36,110,226)

    # Trash
    trashImg = Image.open(os.path.join(imgdir,'tasks/trash.png'))
    Himage.paste(trashImg,(12,280),trashImg)
    text = today_program['normal'][str(current_day)]['Trash']+" / "+today_program['weekend'][str(current_day)]['Trash']
    DrawText(Himage,text,RobotoLight36,110,298)

    # Vacuum cleaner
    vacuumImg = Image.open(os.path.join(imgdir,'tasks/vacuum.png'))
    Himage.paste(vacuumImg,(12,350),vacuumImg)
    text = today_program['normal'][str(current_day)]['Vacuum']+" / "+today_program['weekend'][str(current_day)]['Vacuum']
    DrawText(Himage,text,RobotoLight36,110,366)

    # Table
    tableImg = Image.open(os.path.join(imgdir,'tasks/furniture.png'))
    Himage.paste(tableImg,(12,420),tableImg)
    text = today_program['normal'][str(current_day)]['Table']+" / "+today_program['weekend'][str(current_day)]['Table']
    DrawText(Himage,text,RobotoLight36,110,438)