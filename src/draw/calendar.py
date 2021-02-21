import os
import sys
sys.path.append("..")

from ..ext.google import GetCalendarEvents

from .util import ImageDraw, DrawText, Image, ImageFont, fontdir

def GenerateCalendarCard(start_date,end_date,title,dark):
    CardImage = Image.new('1', (400, 50), 255)
    draw = ImageDraw.Draw(CardImage)

    RobotoLight18 = ImageFont.truetype(os.path.join(fontdir, 'Roboto/Roboto-Light.ttf'), 18)
    RobotoBold18 = ImageFont.truetype(os.path.join(fontdir, 'Roboto/Roboto-Bold.ttf'), 18)

    color = 0
    if dark:
        # Add dark background and set text to white
        color=1
        draw.rectangle((0,0,400,50),fill="black",outline=None)

    start_time = start_date.strftime("%H:%M")
    end_time = end_date.strftime("%H:%M")
    date_start_printed = start_date.strftime("%d/%m")
    date_end_printed = end_date.strftime("%d/%m")

    DrawText(CardImage,start_time,RobotoLight18,5,7,color)
    DrawText(CardImage,end_time,RobotoLight18,5,26,color)
    DrawText(CardImage,date_start_printed,RobotoBold18,65,7,color)
    DrawText(CardImage,date_end_printed,RobotoBold18,65,26,color)

    title = (title[:22] + '...') if len(title) > 22 else title
    DrawText(CardImage,title,RobotoLight18,130,18,color)

    return CardImage

def GenerateCalendarCards(Himage):
    print("Draw cards")
    events = GetCalendarEvents()

    cards = []
    for index,event in enumerate(events):
        if index % 2 == 0:
            dark = False
        else:
            dark = True
        
        new_card = GenerateCalendarCard(event['start_date'],event['end_date'],event['title'],dark)
        cards.append(new_card)

    for index,card in enumerate(cards):
        Himage.paste(card,(400,130+(index*50)))