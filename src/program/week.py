import os
import json
import time
from datetime import date

from .order import GenerateWeekProgramOrder
from ..util import rootdir, programdir

def GenerateWeekProgram():
    file_dir = os.path.join(rootdir,'members.json')
    # Wait for os to get member file
    while not os.path.exists(file_dir):
        time.sleep(500)
        
    config_file = open(file_dir,'r')
    config = json.load(config_file)

    normal_members = config['week']
    weekend_members = config['weekend']

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