import os
from datetime import date
from .util import ImageFont, DrawText, fontdir

def DrawDate(Himage):
    print("Draw Date")
    RobotoBlack96 = ImageFont.truetype(os.path.join(fontdir, 'Roboto/Roboto-Black.ttf'), 96)
    RobotoLight36 = ImageFont.truetype(os.path.join(fontdir, 'Roboto/Roboto-Light.ttf'), 36)
    RobotoLight30 = ImageFont.truetype(os.path.join(fontdir, 'Roboto/Roboto-Light.ttf'), 30)

    day = date.today().strftime("%d")
    month = date.today().strftime("%B")
    day_name = date.today().strftime("%A")
    DrawText(Himage,day,RobotoBlack96,12,10)
    DrawText(Himage,month,RobotoLight36,18,86)
    DrawText(Himage,day_name,RobotoLight30,129,12)