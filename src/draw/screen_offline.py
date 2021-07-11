import os

from .util import Image,ImageFont,imgdir,DrawText,fontdir
from .screen_refresh import RefreshScreen

def RefreshScreenOffline(screen):
    Himage = Image.new('1', (screen.width, screen.height), 255)

    RobotoBold30 = ImageFont.truetype(os.path.join(fontdir, 'Roboto/Roboto-Bold.ttf'), 30)
    RobotoLight18 = ImageFont.truetype(os.path.join(fontdir, 'Roboto/Roboto-Light.ttf'), 18)

    offlineLogo = Image.open(os.path.join(imgdir,'events/internet_off.png'))
    refreshTime = os.getenv('REFRESH_SECONDS_OFFLINE')

    Himage.paste(offlineLogo,(350,140),offlineLogo)
    DrawText(Himage,"Connection internet indisponible",RobotoBold30,180,242)
    DrawText(Himage,"Tentative de re-connection dans "+refreshTime+"s",RobotoLight18,262,288)
    DrawText(Himage,"(servez vous une tasse de café en attendant)",RobotoLight18,224,380)

    RefreshScreen(screen,Himage)