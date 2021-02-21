import os
import datetime
from .util import ImageFont, DrawText, Image, fontdir, imgdir

def DrawAgendaTop(Himage):
    print("Draw Agenda top")
    #Load font
    RobotoLight36 = ImageFont.truetype(os.path.join(fontdir, 'Roboto/Roboto-Light.ttf'), 36)
    RobotoLight18 = ImageFont.truetype(os.path.join(fontdir, 'Roboto/Roboto-Light.ttf'), 18)
    RobotoLight14 = ImageFont.truetype(os.path.join(fontdir, 'Roboto/Roboto-Light.ttf'), 14)
    agendaImg = Image.open(os.path.join(imgdir,'agenda.png'))
    agendaImg.thumbnail((67,67))

    DrawText(Himage,'Agenda',RobotoLight36,557,37)
    DrawText(Himage,'de la famille',RobotoLight18,569,79)
    DrawText(Himage,'Dernière mise à jour : '+datetime.datetime.now().strftime("%H:%M"),RobotoLight14,618,6)
    Himage.paste(agendaImg,(427,30),agendaImg)