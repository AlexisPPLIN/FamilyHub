from .screenType import ScreenType
from .draw.util import Image,ImageFont,imgdir,DrawText,fontdir

class Screen:
    width = 800
    height = 480

    def __init__(self,type,driver = None):
        self.type = type
        self.driver = driver

    def print(self,Himage):
        print("Printing screen...")
        if(self.type == ScreenType.PHYSICAL):
            self.driver.Clear()
            self.driver.display(self.driver.getbuffer(Himage))
        else:
            Himage.save("export.jpg")

    def init(self):
        if(self.type == ScreenType.PHYSICAL):
            self.driver.init()
        print("type screen initialized !")

