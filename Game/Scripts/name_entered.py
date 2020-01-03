import bge
from bge import logic
import re

def name_entered():
    click_sensor = contr.sensors['Click']
    hover_sensor = contr.sensors['Hover']

    if click_sensor.positive and hover_sensor.positive:
        input = logic.getCurrentScene().objects['NameField']['Text']
        matches = re.match('^[A-Za-z0-9_-]+$', input) != None and len(input) > 0 and len(input) <= 15
        if matches:
            logic.globalDict['Name'] = input
            contr = logic.getCurrentController()
            contr.activate(contr.actuators['Scene'])