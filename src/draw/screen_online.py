from .util import Image, DrawGird
from .screen_refresh import RefreshScreen

from .agenda import DrawAgendaTop
from .date import DrawDate
from .weather import DrawWeather
from .task import DrawTasks
from .calendar import GenerateCalendarCards

def RefreshScreenOnline(screen):
    # Generate new screen
    Himage = Image.new('1', (screen.width, screen.height), 255)

    DrawAgendaTop(Himage)
    DrawDate(Himage)
    DrawWeather(Himage)
    DrawTasks(Himage)
    #GenerateCalendarCards(Himage)
    DrawGird(Himage)
    
    RefreshScreen(screen,Himage)