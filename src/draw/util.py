import os

from PIL import Image, ImageDraw, ImageFont, ImageOps
from ..util import fontdir, imgdir

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

def ConvertImage(PilImage):
    bw = PilImage.convert('1',dither=Image.NONE)
    bw.save('test.jpg')
    return bw