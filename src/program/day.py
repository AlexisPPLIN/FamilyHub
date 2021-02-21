import os
import json
from datetime import date

from .week import GenerateWeekProgram
from ..util import programdir

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