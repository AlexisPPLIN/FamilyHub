from __future__ import print_function
import sys
import os
libfir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'FamilyHub/lib')
sys.path.insert(1, libfir)

# Load dotenv
from dotenv import load_dotenv
load_dotenv()

import logging
import locale
import requests
import random
import json
from datetime import date
from waveshare_epd import epd7in5_V2
from PIL import Image, ImageDraw, ImageFont, ImageOps
from pyowm import OWM
from dateutil.parser import parse as dtparse
from twisted.internet import task as ttask, reactor as ttreactor

# Google API
import datetime
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

rootdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'FamilyHub')
fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'FamilyHub/fonts')
imgdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'FamilyHub/images')
programdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'FamilyHub/programs')

locale.setlocale(locale.LC_ALL,'fr_FR.UTF-8')

def DrawText(Himage,text,font,x,y,color=0):
    x = x - font.getoffset(text)[0]
    y = y - font.getoffset(text)[1]
    draw = ImageDraw.Draw(Himage)
    draw.text((x,y),text,font=font,fill=color)

def DrawGird(Himage):
    print("Drawing main frame grid")
    draw = ImageDraw.Draw(Himage)
    draw.line((0,130,800,130)) #Horizontal line
    draw.line((400,0,400,480))

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

def GetLocalWeather():
    owm = OWM(os.getenv("OPEN_WEATHER_APIKEY"))

    # Search for weather
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(os.getenv("WEATHER_PLACE"))
    weather = observation.weather

    return weather.weather_icon_name,weather.temperature('celsius')['temp']

def ConvertImage(PilImage):
    bw = PilImage.convert('1',dither=Image.NONE)
    bw.save('test.jpg')
    return bw

def GetWeatherIcon(WeatherCode):
    code = WeatherCode[0:2]
    time = WeatherCode[2]
    img_path  = ""

    if(code == '01' or code == '02' or code == '10'):
        img_path =  os.path.join(imgdir,'weather/'+code+''+time+'.png')
    else:
        img_path = os.path.join(imgdir,'weather/'+code+'.png')

    if os.path.isfile(img_path):
        return img_path
    else:
        return os.path.join(imgdir,'weather/default.png')
    

def DrawWeather(Himage):
    print("Draw Weather")
    RobotoLight36 = ImageFont.truetype(os.path.join(fontdir, 'Roboto/Roboto-Light.ttf'), 36)

    icon_code, temp = GetLocalWeather()

    weatherImg = Image.open(GetWeatherIcon(icon_code))

    DrawText(Himage,str(temp)+'°',RobotoLight36,288,90)
    Himage.paste(weatherImg,(310,21),weatherImg)

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

def GenerateWeekProgram():
    normal_members = ["Alexis","Lucien","Zéa"]
    weekend_members = ["Alexis","Lucien","Zéa","Lilou","Maëlle"]

    normal_program = GenerateWeekProgramOrder(len(normal_members))
    weekend_program = GenerateWeekProgramOrder(len(weekend_members))

    # Fill each programs with names
    for day in normal_program:
        for task in normal_program[day]:
            index = normal_program[day][task]
            normal_program[day][task] = normal_members[index]

    for day in weekend_program:
        for task in weekend_program[day]:
            index = weekend_program[day][task]
            weekend_program[day][task] = weekend_members[index]
    
    # Create folder (is not exists) to store program in case of reboot
    if not os.path.isdir(programdir):
        os.mkdir(programdir)
    
    # Construct file name
    date_file = date.today().strftime("%V%Y")
    file_name = "program_"+date_file+".json"

    # Generate json
    json_data = {
        "normal": normal_program,
        "weekend" : weekend_program
    }
    json_dumped = json.dumps(json_data,ensure_ascii=False)

    json_file = open(os.path.join(programdir,file_name),"w")
    json_file.write(json_dumped)
    json_file.close()

def GetDayProgram():
    # Search for program in file
    date_file = date.today().strftime("%V%Y")
    file_name = "program_"+date_file+".json"
    file_path = os.path.join(programdir,file_name)

    program_obj = None

    if os.path.isfile(file_path):
        # Load program json
        with open(file_path,"r") as program_file:
            program_text = program_file.read()
        
        # Parse json
        program_obj = json.loads(program_text)
    else:
        GenerateWeekProgram()
        return GetDayProgram()
    
    return program_obj

def DrawTasks(Himage):
    print("Draw day tasks")
    today_program = GetDayProgram()
    current_day = date.today().strftime("%A")

    RobotoLight36 = ImageFont.truetype(os.path.join(fontdir, 'Roboto/Roboto-Light.ttf'), 36)
    RobotoLight14 = ImageFont.truetype(os.path.join(fontdir, 'Roboto/Roboto-Light.ttf'), 14)
    DrawText(Himage,'semaine / week-end',RobotoLight14,113,133)

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

def GetCalendarEvents():
    print('[Calendar API] Get last events')
    creds = None
    tokendir = os.path.join(rootdir, 'token.pickle')
    
    #Check if the user already logged
    if os.path.exists(tokendir):
        with open(tokendir,'rb') as token:
            creds = pickle.load(token)
    
    # If the file doesn't exists, log the user
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.path.join(rootdir, 'credentials.json'), SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(tokendir,'wb') as token:
            pickle.dump(creds,token)
    
    service = build('calendar','v3',credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    print('[Calendar API] Getting the upcoming 7 events')
    events_result = service.events().list(calendarId=os.getenv('CALENDAR_ID'),timeMin=now,maxResults=7,singleEvents=True,orderBy='startTime').execute()

    events = events_result.get('items',[])

    return_events = []

    if not events:
        print('No upcoming events found')
    
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        start_datetime = dtparse(start)
        end_datetime = dtparse(end)

        new_event = {
            "start_date": start_datetime,
            "end_date": end_datetime,
            "title": event["summary"]
        }
        return_events.append(new_event)

    return return_events

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

def RefreshScreen():
    epd.Clear()

    Himage = Image.new('1', (epd.width, epd.height), 255)
    DrawAgendaTop(Himage)
    DrawDate(Himage)
    DrawWeather(Himage)
    DrawTasks(Himage)
    GenerateCalendarCards(Himage)
    DrawGird(Himage)
    epd.display(epd.getbuffer(Himage))
    pass

try:
    epd = epd7in5_V2.EPD()
    print("init and Clear")
    epd.init()

    timeout = float(os.getenv('REFRESH_SECONDS'))
    l = ttask.LoopingCall(RefreshScreen)
    l.start(timeout)

    ttreactor.run()

except IOError as e:
    print(e)
    
except KeyboardInterrupt:    
    print("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit()
    exit()
