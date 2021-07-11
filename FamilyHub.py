from __future__ import print_function
import sys
import os
import logging
import locale
import time
import logging
import traceback

# Load dotenv
from dotenv import load_dotenv
load_dotenv()

from src.screen import Screen
from src.screenType import ScreenType

if(os.getenv('SCREEN_MODE') == "SOFTWARE"):
    print("Running FamilyHub with SOFTWARE screen")
    screen = Screen(ScreenType.SOFTWARE)
elif(os.getenv('SCREEN_MODE') == "PHYSICAL"):
    print("Running FamilyHub with PHYSICAL screen")
    from lib.waveshare_epd import epd7in5_V2
    epd = epd7in5_V2.EPD()
    screen = Screen(ScreenType.PHYSICAL,epd)

libfir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'FamilyHub/lib')
rootdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'FamilyHub')
fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'FamilyHub/fonts')
imgdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'FamilyHub/images')

sys.path.insert(1, libfir)

from src.ext.internet import checkInternetUrllib
from src.draw.screen_offline import RefreshScreenOffline
from src.draw.screen_online import RefreshScreenOnline

locale.setlocale(locale.LC_ALL,'fr_FR.UTF-8')

# -- Main --
try:
    screen.init()

    while True:
        print("Starting printing process...")
        if(checkInternetUrllib()):
            print("-> Online mode")
            RefreshScreenOnline(screen)

            waitingTime = int(os.getenv('REFRESH_SECONDS'))
            print("waiting "+str(waitingTime)+" ms...")
            time.sleep(waitingTime)
        else:
            print("-> Offline mode")
            RefreshScreenOffline(screen)

            waitingTime = int(os.getenv('REFRESH_SECONDS_OFFLINE'))
            print("waiting "+str(waitingTime)+" ms...")
            time.sleep(int(os.getenv('REFRESH_SECONDS_OFFLINE')))
    
except Exception as e:
    print(e)
    traceback.print_exc()
    
except KeyboardInterrupt:    
    print("ctrl + c:")
    exit()