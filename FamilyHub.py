from __future__ import print_function
import sys
import os
import logging
import locale
import time
import bugsnag
import logging

libfir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'FamilyHub/lib')
rootdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'FamilyHub')
fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'FamilyHub/fonts')
imgdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'FamilyHub/images')

sys.path.insert(1, libfir)

# Load dotenv
from dotenv import load_dotenv
load_dotenv()

from lib.waveshare_epd import epd7in5_V2

from src.ext.internet import checkInternetUrllib
from src.draw.screen_offline import RefreshScreenOffline
from src.draw.screen_online import RefreshScreenOnline

locale.setlocale(locale.LC_ALL,'fr_FR.UTF-8')

# Use bugsnag as error reporting tool
from bugsnag.handlers import BugsnagHandler
bugsnag.configure(
    api_key=os.getenv('BUGSNAG_TOKEN'),
    project_root=rootdir,
)

logger = logging.getLogger("logger")
handler = BugsnagHandler()
handler.setLevel(logging.ERROR)
logger.addHandler(handler)


# -- Main --
try:
    epd = epd7in5_V2.EPD()
    print("init and Clear")
    epd.init()

    while True:
        if(checkInternetUrllib()):
            RefreshScreenOnline(epd)
            break
        else:
            RefreshScreenOffline(epd)
            time.sleep(int(os.getenv('REFRESH_SECONDS_OFFLINE')))
    
except Exception as e:
    print(e)
    bugsnag.notify(e)
    
except KeyboardInterrupt:    
    print("ctrl + c:")
    exit()