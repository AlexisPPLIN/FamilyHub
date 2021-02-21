import os

from ..ext.weather import GetLocalWeather
from .util import ImageFont, DrawText, Image, fontdir, imgdir

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