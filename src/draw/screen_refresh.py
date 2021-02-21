def RefreshScreen(epd,Himage):
    # Clear screen
    epd.Clear()
    
    # Display generated screen
    epd.display(epd.getbuffer(Himage))
    pass